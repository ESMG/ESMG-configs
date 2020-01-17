import numpy as np

f = open('expList.txt','r')
h = open('Codes.txt','w')
Seg_001='#override OBC_SEGMENT_003 = \"J=0,I=0:N,'
Seg_002='#override OBC_SEGMENT_002 = \"J=N,I=N:0,'

# Calculate the baroclinic deformation radius for dumbbell
Rho0=1.035e3 # kg m-3
Irho=1.0/Rho0
drho_dS=1.0 # kg m-3 psu-1
grav=9.8 # m s-2
dS=2.0 # psu
F0=1.e-4 # Coriolis parameter
dZ=1.e3 # meters
IdZ=1.0/dZ # meters
pi=3.14
N=np.sqrt(grav*IdZ*(Irho*(dS*drho_dS))) # s-1
Ld=(N*dZ)/(np.pi*F0) # m
#print('N=',N,' s-1')
print('N/f=',N/F0)
print('Deformation Radius(km)= ',Ld*1.e-3)
# The Velocity scale is a typical eddy velocity observed from the parent model
Vscale_in=0.1 # m s-1
#Tscale_in=(Ld/Vscale_in)/8.64e4 # days
Tscale_in=1.0 # days
Vscale_out=0.0001 # m s-1
Tscale_out=300. # days
Lscale_in=1.e3 # m
Lscale_out=5.e3 # m
print('NOTE:Using Incoming Time scale (days)=',Tscale_in)
print('NOTE:Using Incoming Length scale (m)=',Lscale_in)
print('NOTE:Using Outgoing Time scale(days)=',Tscale_out)
print('NOTE:Using Outgoing Length scale(m)=',Lscale_out)


for line in f.readlines():
    line=line.lstrip()
    if len(line)==0:
        continue
    if line[0]=="#":
      continue
    else:
      has_comment=False
      # Separate trailing comments
      if line.find("#")>0:
          comment=line[line.find("#"):]
          line=line[:line.find("#")]
          has_comment=True
      Res=line.split('-')
      exp=Res[0].split(':')
      #print(len(Res),len(exp))
      dict={'Name':exp[0],'Code':exp[1],'BT':Res[1],'BC':Res[2],'Tan':Res[3],'Grad':Res[4],'V':Res[5],'S':Res[6],'Ti':float(Res[7])*Tscale_in,'To':float(Res[8])*Tscale_out,'Li':float(Res[9])*Lscale_in,'Lo':float(Res[10].rstrip())*Lscale_out,'W':float(Res[11])}
      #print(dict)
      if has_comment:
          dict['comment']=comment
      g=open('MOM_override.'+dict['Code'],'w')
      for s in [Seg_001,Seg_002]:
        Str=s
        Str=Str+'NUDGED,'
        if dict['BT']=='S' or dict['BC']=='S':  # NO RADIATION, JUST NUDGING
            Str=Str+'SIMPLE,'
        elif dict['BT']=='F': # Flather for the external model
            Str=Str+'FLATHER,'
        if dict['BC']=='Or':  # Normal radiation for baroclinic flow
            Str=Str+'ORLANSKI,'
        elif dict['BC']=='Ob': # Oblique radiation for baroclinic flow
            Str=Str+'OBLIQUE,'
        if dict['Tan']=='Ob': # Oblique radiation of tangential flow (only useed for computed vorticity)
            Str=Str+'OBLIQUE_TAN,NUDGED_TAN,'
        elif dict['Tan']=='Or': # Oblique radiation of tangential flow (only useed for computed vorticity)
            Str=Str+'ORLANSKI_TAN,NUDGED_TAN,'
        elif dict['Tan']=='S': # Simple nudging tangential flow
            Str=Str+'NUDGED_TAN,'
        if dict['Grad']=='Or': # Normal radiation of kinetic energy gradient
            Str=Str+'ORLANSKI_GRAD,NUDGED_GRAD,'
        elif dict['Grad']=='Ob': # Oblique radiation of kinetic energy gradient
            Str=Str+'OBLIQUE_GRAD,NUDGED_GRAD,'
        elif dict['Grad']=='S': # Oblique radiation of kinetic energy gradient
            Str=Str+'NUDGED_GRAD,'
        if Str[-1]==',':
            Str=Str[:-1]
        g.write(Str+'"\n')
      for s in ['OBC_SEGMENT_003','OBC_SEGMENT_002']:
          Str=s+'_VELOCITY_NUDGING_TIMESCALES = '+str(dict['Ti'])+','+str(dict['To'])+'\n'
          g.write(Str)
      Str='OBC_TRACER_RESERVOIR_LENGTH_SCALE_IN = '+str(dict['Li'])+'\n'
      g.write(Str)
      Str='OBC_TRACER_RESERVOIR_LENGTH_SCALE_OUT = '+str(dict['Lo'])+'\n'
      g.write(Str)
      Str='OBC_RAD_VEL_WT = '+str(dict['W'])+'\n'
      g.write(Str)

      if dict['V']=='F':
          Str='OBC_FREESLIP_VORTICITY = True \n'
          g.write(Str)
          Str='OBC_ZERO_VORTICITY = False \n'
          g.write(Str)
      elif dict['V']=='C':
          Str='OBC_COMPUTED_VORTICITY = True \n'
          g.write(Str)
          Str='OBC_FREESLIP_VORTICITY = False \n'
          g.write(Str)

      elif dict['V']=='S':
          Str='OBC_SPECIFIED_VORTICITY = True \n'
          g.write(Str)
          Str='OBC_FREESLIP_VORTICITY = False \n'
          g.write(Str)
      elif dict['V']=='Z':
          Str='OBC_ZERO_VORTICITY = True \n'
          g.write(Str)
          Str='OBC_FREESLIP_VORTICITY = False \n'
          g.write(Str)
      if dict['S']=='F':
          Str='OBC_FREESLIP_STRAIN = True \n'
          g.write(Str)
          Str='OBC_ZERO_STRAIN = False \n'
          g.write(Str)
      elif dict['S']=='C':
          Str='OBC_FREESLIP_STRAIN = False \n'
          g.write(Str)
          Str='OBC_COMPUTED_STRAIN = True \n'
          g.write(Str)
      elif dict['S']=='S':
          Str='OBC_SPECIFIED_STRAIN = True \n'
          g.write(Str)
          Str='OBC_FREESLIP_STRAIN = False \n'
          g.write(Str)
      elif dict['S']=='Z':
          Str='OBC_ZERO_STRAIN = True \n'
          g.write(Str)
          Str='OBC_FREESLIP_STRAIN = False \n'
          g.write(Str)

      g.close()
      h.write(dict['Code']+'\n')
h.close()
