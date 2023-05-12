# 起動方法
#    開始:  wsadmin.sh -lang jython -host (NAホスト名) -port (NAポート番号) -f tpvLogging.py (AP名) start
#    停止:  wsadmin.sh -lang jython -host (NAホスト名) -port (NAポート番号) -f tpvLogging.py (AP名) stop

import com.ibm.ws.tpv.engine.UserPreferences
import jarray

refreshRate     = 60                # 取得間隔(秒)（最大 500 秒まで)
loggingDuration = 48 * 60 * 60      # 取得期間(秒)
logFileSize     = 100 * 1024 * 1024 # ログ・ファイル・サイズ(byte)
numLogFiles     = 5                 # ログ・ファイル数
bufferSize      = 20                # バッファー・サイズ（設定可能値：10、20、30、40、50、60、70、80、90、100）
logFileName     = "tpv"

print ""
thisCell = AdminControl.getCell()
thisNode = AdminControl.getNode()
print "cell =",thisCell
print "node =",thisNode

if ( len( sys.argv ) < 1 ):
    print "アプリケーション・サーバー名が指定されていません。"
    sys.exit( 4 )
targetServer = sys.argv[0]
print "server =",targetServer
targetServerName = AdminControl.completeObjectName("type=Server,node="+thisNode+",name="+targetServer+",*" )
if ( len( targetServerName ) <= 0 ):
    print "指定されたサーバーは存在しません。"
    sys.exit( 4 )

if ( len( sys.argv ) < 2 ):
    print "TPVの開始(start)または停止(stop)が指定されていません。"
    sys.exit( 4 )
tpvOperation = sys.argv[1]
if ( tpvOperation != "start" and tpvOperation != "stop" ):
    print "TPVの開始(start)または停止(stop)の指定が無効です。"
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
            print "TPV のロギングは既に開始されています。"
        else:
            print "TPV のロギングを開始します。"
            print "params =",params
            AdminControl.invoke_jmx( tpvOName, "monitorServer", params, sigs )
            AdminControl.invoke_jmx( tpvOName, "startLogging",  params, sigs )
            print "TPV のロギングを開始しました。"
    
    if ( tpvOperation == "stop" ):
        if ( AdminControl.invoke_jmx( tpvOName, "isServerLogging", [chkTarget], ["com.ibm.ws.tpv.engine.utils.ServerBean"] ) ):
            print "TPV のロギングを停止します。"
            print "params =",params
            AdminControl.invoke_jmx( tpvOName, "stopLogging",   params, sigs )
            AdminControl.invoke_jmx( tpvOName, "disableServer", params, sigs )
            print "TPV のロギングを停止しました。"
        else:
            print "TPV のロギングは既に停止しています。"
    
    print ""
    # sys.exit( 0 )

except:
    typ, val, tb = sys.exc_info()
    print "エラーが発生しました。"
    print typ
    print val
    print tb
    sys.exit( 16 )
