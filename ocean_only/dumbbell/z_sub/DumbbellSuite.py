import subprocess


param_names=[\
             'Parent',\
             'BtTransport',\
             'BcTransport',\
             'NormalTransportNudge',\
             'TrRes_Lscale',\
             'TrRes_Tscale',\
             'Vort',\
             'Strain',\
             'BiHarmonic']

def parse_names(record,debug=False):
    dict_={}
    meta_=record.split('-')
    if debug: print(meta_)
    for p,m in zip(param_names,meta_):
        dict_[p]=m

    return dict_

def construct_params(pf,record):

    seg_lines=[]
    param_lines=[]

    for pname in param_names:
        meta_=record[pname]
        if pname=='BtTransport':
            if meta_=='S':
                line_="OBC_SEGMENT_001 = \"I=0,J=N:0,SIMPLE\""
                seg_lines.append(line_)
                line_="OBC_SEGMENT_002 = \"I=N,J=N:0,SIMPLE\""
                seg_lines.append(line_)
            if meta_=='F':
                line_="OBC_SEGMENT_001 = \"I=0,J=N:0,FLATHER\""
                seg_lines.append(line_)
                line_="OBC_SEGMENT_002 = \"I=N,J=N:0,FLATHER\""
                seg_lines.append(line_)
        if pname=='BcTransport':
            if meta_[0]=='N':
                line_=seg_lines[0]
                line_=line_[:-1]+",NUDGED\""
                seg_lines.append(line_)
                line2_=seg_lines[1]
                line2_=line2_[:-1]+",NUDGED\""
                seg_lines=[]
                seg_lines.append(line_)
                seg_lines.append(line2_)
            if meta_[1:]=='OR':
                line_=seg_lines[0]
                line_=line_[:-1]+",ORLANSKI\""
                seg_lines.append(line_)
                line2_=seg_lines[1]
                line2_=line2_[:-1]+",ORLANSKI\""
                seg_lines=[]
                seg_lines.append(line_)
                seg_lines.append(line2_)
            if meta_[1:]=='OB':
                line_=seg_lines[0]
                line_=line_[:-1]+",OBLIQUE\""
                seg_lines.append(line_)
                line2_=seg_lines[1]
                line2_=line2_[:-1]+",OBLIQUE\""
                seg_lines=[]
                seg_lines.append(line_)
                seg_lines.append(line2_)
        if pname=='NormalTransportNudge':
            meta__=meta_.split(':')
            line_='OBC_SEGMENT_001_VELOCITY_NUDGING_TIMESCALES = '+str(float(meta__[0]))+','+str(float(meta__[1]))
            seg_lines.append(line_)
            line_='OBC_SEGMENT_002_VELOCITY_NUDGING_TIMESCALES = '+str(float(meta__[0]))+','+str(float(meta__[1]))
            seg_lines.append(line_)
        if pname=='TrRes_Lscale':
            meta__=meta_.split(':')
            line_='OBC_TRACER_RESERVOIR_LENGTH_SCALE_IN = '+str(float(meta__[0]))
            seg_lines.append(line_)
            line_='OBC_TRACER_RESERVOIR_LENGTH_SCALE_OUT = '+str(float(meta__[1]))
            seg_lines.append(line_)
        if pname=='Vort':
            if meta_=='Z':
                line_="OBC_ZERO_VORTICITY = True"
                seg_lines.append(line_)
                line_="OBC_FREESLIP_VORTICITY = False"
                seg_lines.append(line_)
            if meta_=='FS':
                line_="OBC_FREESLIP_VORTICITY = True"
                seg_lines.append(line_)
            if meta_=='C':
                line_="OBC_COMPUTED_VORTICITY = True"
                seg_lines.append(line_)
                line_="OBC_FREESLIP_VORTICITY = False"
                seg_lines.append(line_)
            if meta_=='S':
                line_="OBC_SPECIFIED_VORTICITY = True"
                seg_lines.append(line_)
                line_="OBC_FREESLIP_VORTICITY = False"
                seg_lines.append(line_)
        if pname=='Strain':
            if meta_=='Z':
                line_="OBC_ZERO_STRAIN = True"
                seg_lines.append(line_)
                line_="OBC_FREESLIP_STRAIN = False"
                seg_lines.append(line_)
            if meta_=='FS':
                line_="OBC_FREESLIP_STRAIN = True"
                seg_lines.append(line_)
            if meta_=='C':
                line_="OBC_COMPUTED_STRAIN = True"
                seg_lines.append(line_)
                line_="OBC_FREESLIP_STRAIN = False"
                seg_lines.append(line_)
            if meta_=='S':
                line_="OBC_SPECIFIED_STRAIN = True"
                seg_lines.append(line_)
                line_="OBC_FREESLIP_STRAIN = False"
                seg_lines.append(line_)
        if pname=='BiHarmonic':
            if meta_=='Z':
                line_="OBC_ZERO_BIHARMONIC = True"
                seg_lines.append(line_)
    for s in seg_lines:
        pf.write(s+"\n")

ExpList=['P002-S-N-0:0-0:0-0:0-Z-Z-Z',\
         'P002-S-N-0:0-0:0-0:0-FS-Z-Z',\
         'P002-S-N-0:0-0:0-0:0-Z-FS-Z',\
         'P002-S-N-0:0-0:0-0:0-FS-FS-Z',\
         'P002-F-N-0:0-0:0-0:0-Z-Z-Z',\
         'P002-F-N-0:0-0:0-0:0-FS-Z-Z',\
         'P002-F-N-0:0-0:0-0:0-Z-FS-Z',\
         'P002-F-N-0:0-0:0-0:0-FS-FS-Z',\
         'P002-F-NOR-0.1:0.1-0:0-0:0-Z-Z-Z',\
         'P002-F-NOR-0.1:0.1-0:0-0:0-FS-Z-Z',\
         'P002-F-NOR-0.1:0.1-0:0-0:0-Z-FS-Z',\
         'P002-F-NOR-0.1:0.1-0:0-0:0-FS-FS-Z',\
         'P002-F-NOR-1:1-0:0-0:0-Z-Z-Z',\
         'P002-F-NOR-1:1-0:0-0:0-FS-Z-Z',\
         'P002-F-NOR-1:1-0:0-0:0-Z-FS-Z',\
         'P002-F-NOR-1:1-0:0-0:0-FS-FS-Z',\
         'P002-F-NOB-1:10-0:0-0:0-Z-Z-Z',\
         'P002-F-NOB-1:1-0:0-0:0-FS-Z-Z',\
         'P002-F-NOB-1:1-0:0-0:0-Z-FS-Z',\
         'P002-F-NOB-1:1-0:0-0:0-FS-FS-Z',\
         'P002-F-NOR-0.1:0.1-0:0-0:0-FS-FS-Z',\
         'P002-F-NOR-0.1:1-0:0-0:0-FS-FS-Z',\
         'P002-F-NOR-0.1:2-0:0-0:0-FS-FS-Z',\
         'P002-F-NOR-0.1:0.5-0:0-0:0-FS-FS-Z',\
         'P002-F-NOR-0.1:0.1-1.e2:1.e2-.1:.1-FS-FS-Z',\
         'P002-F-NOR-0.1:0.1-1.e2:1.e3-.1:.1-FS-FS-Z',\
         'P002-F-NOR-0.1:0.1-1.e2:1.e2-.1:1-FS-FS-Z']


for i,exp in enumerate(ExpList):
    mpo=open('MOM_override_'+str(i+1),'w')
    mpo.write("#override SPONGE = False \n")
    mpo.write("#override DAYMAX = 30.0 \n")
    mpo.write("#override WESTLON = -100 \n")
    mpo.write("#override LENLON = 200 \n")
    mpo.write("#override NIGLOBAL = 40 \n")
    mpo.write("#override OBC_NUMBER_OF_SEGMENTS = 2 \n")
    mpo.write("BRUSHCUTTER_MODE = False \n")
    mpo.write("OBC_SEGMENT_001_DATA = \"U=file:west.nc(u),V=file:west.nc(v),SSH=file:west.nc(zeta),SALT=file:west.nc(salt),DVDX=file:west.nc(dvdx)\"\n")
    mpo.write("OBC_SEGMENT_002_DATA = \"U=file:east.nc(u),V=file:east.nc(v),SSH=file:east.nc(zeta),SALT=file:east.nc(salt),DVDX=file:east.nc(dvdx)\"\n")

    ExpParams=parse_names(exp)
    print(ExpParams)
    construct_params(mpo,ExpParams)
    mpo.close()
