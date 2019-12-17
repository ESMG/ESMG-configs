f = open('expList.txt','r')
h = open('Codes.txt','w')
Seg_001='OBC_SEGMENT_001 = \"I=0,J=N:0,'
Seg_002='OBC_SEGMENT_002 = \"I=N,J=0:N,'

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

      dict={'Name':exp[0],'Code':exp[1],'BT':Res[1],'BC':Res[2],'VS':Res[3],'Ti':float(Res[4]),'To':float(Res[5]),'Li':float(Res[6]),'Lo':float(Res[7].rstrip())}
      print(dict)
      if has_comment:
          dict['comment']=comment
      g=open('MOM_override.'+dict['Code'],'w')
      for s in [Seg_001,Seg_002]:
        Str=s
        if dict['BT']=='S':
            Str=Str+'SIMPLE,'
        elif dict['BT']=='F':
            Str=Str+'FLATHER,'
        if dict['BC']=='S':
            Str=Str+'SIMPLE'
        elif dict['BC']=='Or':
            Str=Str+'ORLANSKI'
        elif dict['BC']=='Ob':
            Str=Str+'OBLIQUE'
        g.write(Str+'"\n')
      for s in ['OBC_SEGMENT_001_','OBC_SEGMENT_002_']:
          Str=s+'_VELOCITY_NUDGING_TIMESCALES = '+str(dict['Ti'])+','+str(dict['To'])+'\n'
          g.write(Str)
      Str='OBC_TRACER_RESERVOIR_LENGTH_SCALE_IN = '+str(dict['Li'])+'\n'
      g.write(Str)
      Str='OBC_TRACER_RESERVOIR_LENGTH_SCALE_OUT = '+str(dict['Lo'])+'\n'
      g.write(Str)

      if dict['VS']=='F':
          Str='OBC_FREESLIP_VORTICITY = True \n'
          g.write(Str)
          Str='OBC_ZERO_VORTICITY = False \n'
          g.write(Str)
          Str='OBC_FREESLIP_STRAIN = True \n'
          g.write(Str)
          Str='OBC_ZERO_STRAIN = False \n'
          g.write(Str)
      elif dict['VS']=='C':
          Str='OBC_COMPUTED_VORTICITY = True \n'
          g.write(Str)
          Str='OBC_ZERO_VORTICITY = False \n'
          g.write(Str)
          Str='OBC_FREESLIP_VORTICITY = False \n'
          g.write(Str)
          Str='OBC_COMPUTED_STRAIN = True \n'
          g.write(Str)
          Str='OBC_ZERO_STRAIN = False \n'
          g.write(Str)
          Str='OBC_FREESLIP_STRAIN = False \n'
          g.write(Str)
      elif dict['VS']=='S':
          Str='OBC_SPECIFIED_VORTICITY = True \n'
          g.write(Str)
          Str='OBC_ZERO_VORTICITY = False \n'
          g.write(Str)
          Str='OBC_FREESLIP_VORTICITY = False \n'
          g.write(Str)
          Str='OBC_SPECIFIED_STRAIN = True \n'
          g.write(Str)
          Str='OBC_ZERO_STRAIN = False \n'
          g.write(Str)
          Str='OBC_FREESLIP_STRAIN = False \n'
          g.write(Str)

      g.close()
      h.write(dict['Code']+'\n')
h.close()
