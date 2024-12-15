# This file is part of atooms
# Copyright 2010-2024, Daniele Coslovich

"""
Base and total interaction class.

Actual interaction backends should implement this interface or
subclass Interaction by implementing the compute() method and
specifying the variables passed to it using the Interaction.variables
dictionary.
"""

import numpy


class InteractionBase(object):

    def __init__(self):
        self.variables = {'position': 'particle.position'}
        """
        A dictionary of variables needed to compute the interaction

        The keys must match the variable names in the
        `Interaction.compute()` interface, the fields must be
        canonicalizable variables accepted by `System.dump()`.

        It is possible to specify the required data type using the
        optionl colon syntax <property>[:<dtype>]. The dtype must a
        valid identifier for numpy array creation.
        """
        # TODO: order is not a good variable, we should expand the syntax using [:order]
        self.order = 'F'  # deprecated
        self.observable = ['energy', 'forces', 'virial', 'stress', 'hessian']
        for observable in self.observable:
            setattr(self, observable, None)

    def __add__(self, other):
        total = Interaction()
        for attr in self.observable:
            if getattr(self, attr, None) is None or getattr(other, attr, None) is None:
                continue
            elif getattr(self, attr) is not None and getattr(other, attr) is not None:
                # Store the sum of the properties in the total interaction
                setattr(total, attr, getattr(self, attr) + getattr(other, attr))
            else:
                raise ValueError('attribute {} not set in {} or {}'.format(attr,
                                                                           self,
                                                                           other))
        return total

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def compute(self, observable, position):
        """
        Compute an `observable` from this interaction

        Subclasses must adapt the interface so as to match the keys
        specified by the `Interaction.variables` dict.
        """
        # Sanity checks
        assert observable in self.observable, \
            'unsupported observable {}'.format(observable)

        # Zeroing observables
        ndim, N = position.shape
        if observable == 'energy':
            self.energy = 0.0
        elif observable == 'forces' or observable is None:
            self.energy = 0.0
            self.virial = 0.0
            self.forces = numpy.zeros_like(position)
        elif observable == 'stress':
            self.energy = 0.0
            self.virial = 0.0
            self.forces = numpy.zeros_like(position)
            self.stress = numpy.zeros(ndim, ndim)
        elif observable == 'hessian':
            self.hessian = numpy.zeros((ndim, N, ndim, N))


class Interaction(InteractionBase):

    def __init__(self, *terms):
        InteractionBase.__init__(self)
        self.variables = {}
        self.term = []
        for term in terms:
            self.add(term)

    def add(self, term):
        self.term.append(term)
        self.variables.update(term.variables)

    def compute(self, observable, **kwargs):
        """
        Compute an `observable` from all terms of this interaction
        """
        if len(self.term) == 0:
            return

        for term in self.term:
            # Extract the relevant variables for this term
            term_kwargs = {}
            for key in term.variables:
                term_kwargs[key] = kwargs[key]
            term.compute(observable, **term_kwargs)

        # Sum all interaction terms
        total = sum(self.term)
        for attr in self.observable:
            setattr(self, attr, getattr(total, attr))


class InteractionWall(InteractionBase):

    def __init__(self, wall, potential):
        InteractionBase.__init__(self)
        self.potential = potential
        if not isinstance(wall, (list, tuple)):
            self.wall = [wall]
        else:
            self.wall = wall
        self.variables = {'pos': 'particle.position',
                          'ids': 'particle.species:int32'}

    def compute(self, observable, pos, ids):
        assert observable in ['forces', 'energy', None]
        if self.forces is None:
            self.forces = numpy.empty_like(pos, order='F')
        self.energy, self.virial, self.forces[:, :] = 0.0, 0.0, 0.0
        N = len(ids)
        # These arrays could be cached
        u, w, h = numpy.ndarray(N), numpy.ndarray(N), numpy.ndarray(N)
        for wall in self.wall:
            rij = wall.distance(pos)
            rsq = numpy.sum(rij**2, axis=0)
            self.potential(rsq, u, w, h)
            self.energy += numpy.sum(u)
            self.forces += w[:] * rij[:, :]

            
class InteractionField(InteractionBase):

    def __init__(self, field, variables=None):
        InteractionBase.__init__(self)
        self.field = field
        self.variables = variables
        if variables is None:
            self.variables = {'pos': 'particle.position'}

    def compute(self, observable, **variables):
        assert 'pos' in variables
        assert observable in ['forces', 'energy', None]
        if self.forces is None:
            self.forces = numpy.empty_like(variables['pos'], order='F')
        u, grad, _ = self.field(**variables)
        self.energy = numpy.sum(u)
        self.virial = 0.0
        self.forces = - grad[:, :]
            
