# �N�����@
#    wsadmin.sh -lang jython -host (DM�z�X�g��) -port (DM�|�[�g�ԍ�) -f pmiSetupForND.py (AP�m�[�h��) (AP��)

newValList = []
newValList.append( { "name": "connectionPoolModule",  "val": "[[enable 6,5,2,1,8,13]]" } )
newValList.append( { "name": "j2cModule",             "val": "[[enable 6,5,2,1,8,13]]" } )
newValList.append( { "name": "threadPoolModule",      "val": "[[enable 3,4]]"      } )
newValList.append( { "name": "servletSessionsModule", "val": "[[enable 7]]"        } )

print ""
thisCell = AdminControl.getCell()
print "cell =",thisCell

if ( len( sys.argv ) < 1 ):
    print "�A�v���P�[�V�����E�T�[�o�[�����݂���m�[�h�̖��O���w�肳��Ă��܂���B"
    sys.exit( 4 )
serverNode = sys.argv[0]
print "node =",serverNode
nodeId = AdminConfig.getid( "/Cell:" + thisCell + "/Node:" + serverNode + "/" )
if ( len( nodeId ) <= 0 ):
    print "�w�肳�ꂽ�m�[�h�͑��݂��܂���B"
    sys.exit( 4 )

if ( len( sys.argv ) < 2 ):
    print "�A�v���P�[�V�����E�T�[�o�[�����w�肳��Ă��܂���B"
    sys.exit( 4 )
serverName = sys.argv[1]
print "server =",serverName
serverId = AdminConfig.getid( "/Cell:" + thisCell + "/Node:" + serverNode + "/Server:" + serverName + "/" )
if ( len( serverId ) <= 0 ):
    print "�w�肳�ꂽ�T�[�o�[�͑��݂��܂���B"
    sys.exit( 4 )

try:
    pmiService = AdminConfig.list( "PMIService", serverId )
    pmiModule  = AdminConfig.list( "PMIModule",  serverId )
    pmiModList = AdminConfig.showAttribute( pmiModule , "pmimodules" ).replace("[","").replace("]","").split(" ")
    
    # PMI �̓��v�Z�b�g���J�X�^���ɕύX
    print ""
    oldVal = AdminConfig.showAttribute( pmiService, "statisticSet" )
    AdminConfig.modify( pmiService, [ [ "enable", "true" ], [ "statisticSet", "custom" ] ] )
    newVal = AdminConfig.showAttribute( pmiService, "statisticSet" )
    print "���v�Z�b�g���J�X�^���ɕύX���܂����B[", oldVal, "]->[", newVal, "]"
    
    # �S�Ă� PMI ���W���[���́A�S�ẴJ�E���^�[�𖳌���
    print ""
    for m in pmiModList:
        modName = AdminConfig.showAttribute( m, "moduleName" )
        oldVal = AdminConfig.showAttribute( m, "enable" )
        AdminConfig.modify( m, "[[ enable '']]" )
        newVal = AdminConfig.showAttribute( m, "enable" )
        print modName, "�̑S�ẴJ�E���^�[�𖳌������܂����B[", oldVal, "]->[", newVal, "]"
    
    # ����̃J�E���^�[��L����
    print ""
    for m in pmiModList:
        modName = AdminConfig.showAttribute( m, "moduleName" )
        for v in newValList:
            if modName == v["name"]:
                oldVal = AdminConfig.showAttribute( m, "enable" )
                AdminConfig.modify( m,  v["val"])
                newVal = AdminConfig.showAttribute( m, "enable" )
                print modName, "�̎w��̃J�E���^�[��L�������܂����B[", oldVal, "]->[", newVal, "]"
    
    
    # �ύX���e��ۑ� (ND�\���̏ꍇ�́A�ʓr�A���������K�v)
    print ""
    AdminConfig.save()
    print "�\����ۊǂ��܂����B�\���𓯊������A�A�v���P�[�V�����E�T�[�o�[���ċN�����Ă��������B"
    
    print ""
    # sys.exit( 0 )
    
except:
    typ, val, tb = sys.exc_info()
    print "�G���[���������܂����B"
    print typ
    print val
    print tb
    sys.exit( 16 )
