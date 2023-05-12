# �N�����@
#    �J�n:  wsadmin.sh -lang jython -host (NA�z�X�g��) -port (NA�|�[�g�ԍ�) -f tpvLogging.py (AP��) start
#    ��~:  wsadmin.sh -lang jython -host (NA�z�X�g��) -port (NA�|�[�g�ԍ�) -f tpvLogging.py (AP��) stop

import com.ibm.ws.tpv.engine.UserPreferences
import jarray

refreshRate     = 60                # �擾�Ԋu(�b)�i�ő� 500 �b�܂�)
loggingDuration = 48 * 60 * 60      # �擾����(�b)
logFileSize     = 100 * 1024 * 1024 # ���O�E�t�@�C���E�T�C�Y(byte)
numLogFiles     = 5                 # ���O�E�t�@�C����
bufferSize      = 20                # �o�b�t�@�[�E�T�C�Y�i�ݒ�\�l�F10�A20�A30�A40�A50�A60�A70�A80�A90�A100�j
logFileName     = "tpv"

print ""
thisCell = AdminControl.getCell()
thisNode = AdminControl.getNode()
print "cell =",thisCell
print "node =",thisNode

if ( len( sys.argv ) < 1 ):
    print "�A�v���P�[�V�����E�T�[�o�[�����w�肳��Ă��܂���B"
    sys.exit( 4 )
targetServer = sys.argv[0]
print "server =",targetServer
targetServerName = AdminControl.completeObjectName("type=Server,node="+thisNode+",name="+targetServer+",*" )
if ( len( targetServerName ) <= 0 ):
    print "�w�肳�ꂽ�T�[�o�[�͑��݂��܂���B"
    sys.exit( 4 )

if ( len( sys.argv ) < 2 ):
    print "TPV�̊J�n(start)�܂��͒�~(stop)���w�肳��Ă��܂���B"
    sys.exit( 4 )
tpvOperation = sys.argv[1]
if ( tpvOperation != "start" and tpvOperation != "stop" ):
    print "TPV�̊J�n(start)�܂��͒�~(stop)�̎w�肪�����ł��B"
    sys.exit( 4 )

try:
    
    tpvName = AdminControl.completeObjectName("type=TivoliPerfEngine,node="+thisNode+",*" )
    tpvOName = AdminControl.makeObjectName(tpvName)
    # print "tpvName=",tpvName
    # print "tpvOName=",tpvOName
    
    chkTarget = com.ibm.ws.tpv.engine.utils.ServerBean( thisNode, targetServer )
    
    pref = com.ibm.ws.tpv.engine.UserPreferences()
    pref.setUserId(          "tpvLogging"    )
    pref.setServerName(      targetServer    )
    pref.setNodeName(        thisNode        )
    pref.setRefreshRate(     refreshRate     )
    pref.setLoggingDuration( loggingDuration )
    pref.setLogFileSize(     logFileSize     )
    pref.setNumLogFiles(     numLogFiles     )
    pref.setBufferSize(      bufferSize      )
    pref.setLogFileName(     logFileName     )
    params=[pref]
    # print params
    
    list_s = java.util.ArrayList()
    list_s.add( "com.ibm.ws.tpv.engine.UserPreferences" )
    sigs = jarray.array( list_s, java.lang.String )
    
    print ""
    if ( tpvOperation == "start" ):
        if ( AdminControl.invoke_jmx( tpvOName, "isServerLogging", [chkTarget], ["com.ibm.ws.tpv.engine.utils.ServerBean"] ) ):
            print "TPV �̃��M���O�͊��ɊJ�n����Ă��܂��B"
        else:
            print "TPV �̃��M���O���J�n���܂��B"
            print "params =",params
            AdminControl.invoke_jmx( tpvOName, "monitorServer", params, sigs )
            AdminControl.invoke_jmx( tpvOName, "startLogging",  params, sigs )
            print "TPV �̃��M���O���J�n���܂����B"
    
    if ( tpvOperation == "stop" ):
        if ( AdminControl.invoke_jmx( tpvOName, "isServerLogging", [chkTarget], ["com.ibm.ws.tpv.engine.utils.ServerBean"] ) ):
            print "TPV �̃��M���O���~���܂��B"
            print "params =",params
            AdminControl.invoke_jmx( tpvOName, "stopLogging",   params, sigs )
            AdminControl.invoke_jmx( tpvOName, "disableServer", params, sigs )
            print "TPV �̃��M���O���~���܂����B"
        else:
            print "TPV �̃��M���O�͊��ɒ�~���Ă��܂��B"
    
    print ""
    # sys.exit( 0 )

except:
    typ, val, tb = sys.exc_info()
    print "�G���[���������܂����B"
    print typ
    print val
    print tb
    sys.exit( 16 )
