#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os

##############################################################################
# get version from path

def version_cmd(i):

    ck=i['ck_kernel']

    fp=i['full_path']

    ver=''

    p0=os.path.basename(fp)
    p1=os.path.dirname(fp)

    lst=os.listdir(p1)
    for fn in lst:
        if fn.startswith(p0):
           x=fn[len(p0):]
           if x.startswith('.'):
              ver=x[1:]
              break

    return {'return':0, 'cmd':'', 'version':ver}

##############################################################################
# setup environment setup

def setup(i):
    """
    Input:  {
              cfg              - meta of this soft entry
              self_cfg         - meta of module soft
              ck_kernel        - import CK kernel module (to reuse functions)

              host_os_uoa      - host OS UOA
              host_os_uid      - host OS UID
              host_os_dict     - host OS meta

              target_os_uoa    - target OS UOA
              target_os_uid    - target OS UID
              target_os_dict   - target OS meta

              target_device_id - target device ID (if via ADB)

              tags             - list of tags used to search this entry

              env              - updated environment vars from meta
              customize        - updated customize vars from meta

              deps             - resolved dependencies for this soft

              interactive      - if 'yes', can ask questions, otherwise quiet
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    # Get variables
    ck=i['ck_kernel']
    s=''

    iv=i.get('interactive','')

    cus=i.get('customize',{})
    fp=cus.get('full_path','')

    p0=os.path.basename(fp)
    p1=os.path.dirname(fp)
    pi=os.path.dirname(p1)

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    win=tosd.get('windows_base','')
    winh=hosd.get('windows_base','')

    # Check platform
    hplat=hosd.get('ck_name','')
    tplat=tosd.get('ck_name','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    remote=tosd.get('remote','')
    tbits=tosd.get('bits','')

    env=i['env']

    found=False
    while True:
       if os.path.isdir(os.path.join(pi,'lib')):
          found=True
          break
       pix=os.path.dirname(pi)
       if pix==pi:
          break
       pi=pix

    if not found:
       return {'return':1, 'error':'can\'t find root dir of Boost installation'}

    ep=cus['env_prefix']
    env[ep]=pi

    cus['path_lib']=p1
    cus['path_include']=os.path.join(pi,'include')

    r = ck.access({'action': 'lib_path_export_script', 
                   'module_uoa': 'os', 
                   'host_os_dict': hosd, 
                   'lib_path': cus.get('path_lib', '')})
    if r['return']>0: return r
    s += r['script']

    ############################################################
    # Setting environment depending on the platform
    if tplat=='win':
       # Check if has dll and then add to PATH
       fpd=fp
       if fp.endswith('.lib'):
          fpd=fp[:-4]+'.dll'
       if fpd.endswith('.dll') and os.path.isfile(fpd):
          s+='\nset PATH='+p1+';%PATH%\n\n'

       env[ep+'_LFLAG_SYSTEM']=os.path.join(p1,'boost_system-mt.lib')
       env[ep+'_LFLAG_THREAD']=os.path.join(p1,'boost_thread-mt.lib')
       env[ep+'_LFLAG_DATE_TIME']=os.path.join(p1,'boost_date_time-mt.lib')
       env[ep+'_LFLAG_FILESYSTEM']=os.path.join(p1,'boost_filesystem-mt.lib')
    else:
       env[ep+'_LFLAG_SYSTEM']='-lboost_system'

    return {'return':0, 'bat':s}
