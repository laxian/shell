

# flutter clean
# flutter packages get
flutter build ios --release

# Mock jenkins env. Remove when commit.
export JOB_NAME=online-live-ios
export WORKSPACE=.
export BUILD_NUMBER=21

cd ./ios

export ETT_APP_NAME=wangxiao
# export ETT_VERSION_PRO=`/usr/bin/agvtool mvers -terse1`
export ETT_VERSION_PRO=V1.0.2
export ETT_WORKSPACE_NAME=Runner
export ETT_SCHEME=Runner
export ETT_BUILD_TYPE=.Release
export ETT_CONFIGURATION=Release

###############################################################################################################
export ETT_JENKINS_TIME=$(date +%m%d) 
export ETT_GIT_COMMIT=${GIT_COMMIT:0:7}
export ETT_GIT_REV=`git rev-list HEAD | wc -l | awk '{print $1}'`
export ETT_VERSION_NUMBER=$ETT_VERSION_PRO$ETT_BUILD_TYPE
export ETT_BUILD_ID=$ETT_VERSION_NUMBER-$ETT_JENKINS_TIME-$BUILD_NUMBER-$ETT_GIT_COMMIT-$ETT_GIT_REV

export NEXUS_JENKINS_NAME=jenkins
export NEXUS_JENKINS_PASSWD=jenkins20100328

# export IPA_Folder=/Users/xxx/Documents/$JOB_NAME/$BUILD_NUMBER
export ExportOptionsPlistPath=./ExportOptions.plist
export XCODE=/usr/bin
export ETT_DIST_ROOT_PATH=../build/ios/$JOB_NAME
export ETT_EXPORT_PATH=$ETT_DIST_ROOT_PATH/$BUILD_NUMBER
export ETT_ARCHIVE_PATH=$ETT_EXPORT_PATH/$ETT_APP_NAME.xcarchive
export ETT_WORK_SPACE=$WORKSPACE/$ETT_WORKSPACE_NAME.xcworkspace

export ETT_FILE_NAME=$ETT_APP_NAME-$ETT_BUILD_ID
export ETT_IPA_NAME=$ETT_FILE_NAME.ipa

echo "============== archive =================="
xcodebuild archive  -workspace $ETT_WORK_SPACE \
                    -scheme $ETT_SCHEME \
                    -configuration "$ETT_CONFIGURATION" \
                    -archivePath $ETT_ARCHIVE_PATH

# export ipa
echo "============== export =================="
xcodebuild -exportArchive -archivePath $ETT_ARCHIVE_PATH \
                          -exportPath $ETT_EXPORT_PATH \
                          -exportOptionsPlist $ExportOptionsPlistPath


echo 'ETT EXPORT PATH: ------>'
echo $ETT_EXPORT_PATH
curl -v -u $NEXUS_JENKINS_NAME:$NEXUS_JENKINS_PASSWD --upload-file $ETT_EXPORT_PATH/Runner.ipa  http://192.168.10.x:xxxx/nexus/service/local/repositories/EttAppReleases/content/com/xxx/$ETT_APP_NAME/ios/$ETT_IPA_NAME