# 起動方法
#    wsadmin.sh -lang jython -host (ホスト名) -port (SOAPポート番号) -f pmiSetupForBASE.py (AP名)

newValList = []
newValList.append( { "name": "connectionPoolModule",  "val": "[[enable 6,5,2,1,8,13]]" } )
newValList.append( { "name": "j2cModule",             "val": "[[enable 6,5,2,1,8,13]]" } )
newValList.append( { "name": "threadPoolModule",      "val": "[[enable 3,4]]"      } )
newValList.append( { "name": "servletSessionsModule", "val": "[[enable 7]]"        } )

print ""
thisCell = AdminControl.getCell()
thisNode = AdminControl.getNode()
print "cell =",thisCell
print "node =",thisNode

if ( len( sys.argv ) < 1 ):
    print "アプリケーション・サーバー名が指定されていません。"
    sys.exit( 4 )
serverName = sys.argv[0]
print "server =",serverName
serverId = AdminConfig.getid( "/Cell:" + thisCell + "/Node:" + thisNode + "/Server:" + serverName + "/" )
if ( len( serverId ) <= 0 ):
    print "指定されたサーバーは存在しません。"
    sys.exit( 4 )

try:
    pmiService = AdminConfig.list( "PMIService", serverId )
    pmiModule  = AdminConfig.list( "PMIModule",  serverId )
    pmiModList = AdminConfig.showAttribute( pmiModule , "pmimodules" ).replace("[","").replace("]","").split(" ")
    
    # PMI の統計セットをカスタムに変更
    print ""
    oldVal = AdminConfig.showAttribute( pmiService, "statisticSet" )
    AdminConfig.modify( pmiService, [ [ "enable", "true" ], [ "statisticSet", "custom" ] ] )
    newVal = AdminConfig.showAttribute( pmiService, "statisticSet" )
    print "統計セットをカスタムに変更しました。[", oldVal, "]->[", newVal, "]"
    
    # 全ての PMI モジュールの、全てのカウンターを無効化
    print ""
    for m in pmiModList:
        modName = AdminConfig.showAttribute( m, "moduleName" )
        oldVal = AdminConfig.showAttribute( m, "enable" )
        AdminConfig.modify( m, "[[ enable '']]" )
        newVal = AdminConfig.showAttribute( m, "enable" )
        print modName, "の全てのカウンターを無効化しました。[", oldVal, "]->[", newVal, "]"
    
    # 特定のカウンターを有効化
    print ""
    for m in pmiModList:
        modName = AdminConfig.showAttribute( m, "moduleName" )
        for v in newValList:
            if modName == v["name"]:
                oldVal = AdminConfig.showAttribute( m, "enable" )
                AdminConfig.modify( m,  v["val"])
                newVal = AdminConfig.showAttribute( m, "enable" )
                print modName, "の指定のカウンターを有効化しました。[", oldVal, "]->[", newVal, "]"
    
    
    # 変更内容を保存 (ND構成の場合は、別途、同期化が必要)
    print ""
    AdminConfig.save()
    print "構成を保管しました。アプリケーション・サーバーを再起動してください。"
    
    print ""
    # sys.exit( 0 )
    
except:
    typ, val, tb = sys.exc_info()
    print "エラーが発生しました。"
    print typ
    print val
    print tb
    sys.exit( 16 )
