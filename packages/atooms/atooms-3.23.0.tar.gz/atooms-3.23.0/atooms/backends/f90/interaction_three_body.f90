 
module interaction

  use helpers
  use cutoff  !, only: is_zero, smooth, adjust
  use potential  !, only: compute
  
  implicit none

contains

  subroutine forces(zero,box,pos,ids,rad,for,epot,virial)
    logical,          intent(in)    :: zero ! to set variables to zero
    double precision, intent(in)    :: box(:)
    double precision, intent(in)    :: pos(:,:)
    integer,          intent(in)    :: ids(:)
    double precision, intent(in)    :: rad(:)
    double precision, intent(inout) :: for(:,:)
    double precision, intent(inout) :: epot, virial
    double precision                :: rij(size(pos,1)), rijsq
    double precision                :: rik(size(pos,1)), riksq
    double precision                :: rjk(size(pos,1)), rjksq
    double precision                :: uijk, wijk, hbox(size(pos,1)), hijk, cos_theta_ijk
    double precision                :: aijk, aij, aik, sin_theta_ijk
    integer                         :: i, j, jj, k, isp, jsp, jjsp, ksp
    logical                         :: zero_ij, zero_ik, zero_jk
    double precision, parameter :: SMALL = 1e-10
    ! TODO: it should be possible to adjust the cutoff from python, but the compute interface is not parsed correctly
    !call adjust(compute)
    for = 0.0d0
    epot = 0.0d0
    virial = 0.0d0
    hbox = box / 2
    do j = 1,size(pos,2)
       do i = j+1,size(pos,2)
       !do j = 1,size(pos,2)
          jsp = ids(j)
          isp = ids(i)
          call distance(i,j,pos,rij)
          call pbc(rij,box,hbox)
          call dot(rij,rij,rijsq)
          call is_zero(isp,jsp,rijsq,zero_ij)
          do k = i+1,size(pos,2)
             ksp = ids(k)
             call distance(i,k,pos,rik)             
             jj = j  ! This is a hack to make inline work
             call distance(jj,k,pos,rjk)
             call pbc(rik,box,hbox)
             call pbc(rjk,box,hbox)
             call dot(rik,rik,riksq)
             call dot(rjk,rjk,rjksq)
             call is_zero(isp,ksp,riksq,zero_ik)
             jjsp = jsp  ! This is a hack to make inline work
             call is_zero(jjsp,ksp,rjksq,zero_jk)
             if (.not.zero_ij .and. .not.zero_ik .and. .not.zero_jk) then
                cos_theta_ijk = dot_product(rij,rik) / sqrt(rijsq * riksq)
                sin_theta_ijk = sqrt(1 - cos_theta_ijk**2) 
                if (sin_theta_ijk < SMALL) sin_theta_ijk = SMALL
                ! s = 1.0/s;
                ! TODO: remove hij via interface             
                !call compute_three_body(isp,jsp,ksp,rijsq,riksq,cos_theta_ijk,uijk,wijk,hijk) ! wij = -(du/dr)/r
                !call smooth_three_body(isp,jsp,ksp,rijsq,uij,wij,hij) ! wij = -(du/dr)/r
                call compute(isp,jsp,ksp,rijsq,riksq,rjksq,cos_theta_ijk,uijk,wijk,hijk) 
                ! call smooth(isp,jsp,ksp,rijsq,uijk,wijk,hijk) ! wij = -(du/dr)/r
                epot = epot + uijk
                print*, i, j, k, uijk, acos(cos_theta_ijk) / (3.1415*2) * 360
                wijk = wijk / sin_theta_ijk
                aijk = - 1 / sqrt(rijsq*riksq)
                aij = cos_theta_ijk / rijsq
                aik = cos_theta_ijk / riksq
                for(:,i) = for(:,i) - wijk * (aij*rij + aik*rik + aijk*rij + aijk*rik)
                for(:,j) = for(:,j) + wijk * (aij*rij + aijk*rik)
                for(:,k) = for(:,k) + wijk * (aij*rik + aijk*rij)
                !print*, '----------'
                !print*, for(:,i)
                !print*, for(:,j)
                !print*, for(:,k)

                virial = virial + wijk * rijsq
             end if
          end do
       end do
    end do
    !epot = epot / 2
    !for = for / 2
  end subroutine forces
  
end module interaction

module interaction_neighbors

  use helpers
  use cutoff  !, only: is_zero, smooth, adjust
  use potential  !, only: compute
  
  implicit none

contains

  subroutine forces(box,pos,ids,neighbors,number_neighbors,for,epot,virial)
    double precision, intent(in)    :: box(:)
    double precision, intent(in)    :: pos(:,:)
    integer,          intent(in)    :: ids(:)
    integer,          intent(in)    :: neighbors(:,:), number_neighbors(:)
    double precision, intent(inout) :: for(:,:)
    double precision, intent(out)   :: epot, virial
    double precision                :: rij(size(pos,1)), rijsq, uij, wij, hbox(size(pos,1)), hij
    integer                         :: i, j, isp, jsp, jn, kn, jj, kk
    logical                         :: zero_ij
    for = 0.0d0
    epot = 0.0d0
    virial = 0.0d0
    hbox = box / 2
    do i = 1,size(pos,2)
       isp = ids(i)
       do jn = 1,number_neighbors(i)
          j = neighbors(jn,i)
          jsp = ids(j)
       end do
    end do
  end subroutine forces

end module interaction_neighbors

