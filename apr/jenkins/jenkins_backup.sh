#!/bin/bash -ex

export GRADLE_HOME=/opt/gradle-5.6.4
export PATH=$GRADLE_HOME/bin:$PATH


CODE_DIR="/home/hdisk1/mengpengfei/GX/code/GX/app/app-apr-food-deliver-meituan"



RELEASE_NOTES_PATH="/home/hdisk/user/mengpengfei/Release_notes"
LAST_COMMIT=`cat ${RELEASE_NOTES_PATH}/app-apr-food-deliver-meituan/commit.log | sed 's/=//g'`
LAST_VERSION=`cat ${RELEASE_NOTES_PATH}/app-apr-food-deliver-meituan/version | awk -F'.' '{print $3}'`

####RobotSelfCheck BUILD########
echo "app-apr-food-deliver build"
cd $CODE_DIR

git checkout -f .
git pull

cp $RELEASE_NOTES_PATH/app-apr-food-deliver-meituan/commit.log $RELEASE_NOTES_PATH/app-apr-food-deliver-meituan/buildinfo/commit.log
gitlab_app-apr-food-deliver_release_notes

NEW_COMMIT=`git rev-parse HEAD`

#if [ ${LAST_COMMIT} != ${NEW_COMMIT} ]
#then


GIT_REV=`git rev-parse --short HEAD`
echo $GIT_REV



VERSION_NAME="1.0.$(( $LAST_VERSION + 1 )).$GIT_REV"
VERSION_CODE="1000$(( $LAST_VERSION + 1 ))"

DATE=`date +%Y%m%d_%H%M_$VERSION_NAME`
echo $DATE



SERVICE_ALL_APK=/home/hdisk1/mengpengfei/GX/smb_dir/gx_app/meituan/$DATE



#sed -i "s/versionCode.*/versionCode $VERSION_CODE/g" meituan/build.gradle
#sed -i "s/versionName.*/versionName \"$VERSION_NAME\"/g" meituan/build.gradle

#sed -i "s/versionCode.*/versionCode $VERSION_CODE/g" express/build.gradle
#sed -i "s/versionName.*/versionName \"$VERSION_NAME\"/g" express/build.gradle

sed -i "s/versionCode.*/versionCode $VERSION_CODE/g" daemon/build.gradle
sed -i "s/versionName.*/versionName \"$VERSION_NAME\"/g" daemon/build.gradle

sed -i "s/versionCode.*/versionCode $VERSION_CODE/g" app/build.gradle
sed -i "s/versionName.*/versionName \"$VERSION_NAME\"/g" app/build.gradle

#sed -i '/<manifest/a android:sharedUserId="android.uid.system"' app/src/main/AndroidManifest.xml

#echo "gradle clean"
gradle -Dorg.gradle.java.home=/home/hdisk/user/mengpengfei/tools/android-studio/jre/ clean
gradle -Dorg.gradle.java.home=/home/hdisk/user/mengpengfei/tools/android-studio/jre/ build


mkdir -p $SERVICE_ALL_APK	





#cp -f meituan/build/outputs/apk/debug/meituan-web-debug.apk $SERVICE_ALL_APK/meituan-web-debug-$VERSION_NAME.apk
#cp -f express/build/outputs/apk/debug/segway-express-debug.apk $SERVICE_ALL_APK/segway-express-debug-$VERSION_NAME.apk
cp -f app/build/outputs/apk/debug/segway-delivery-debug.apk $SERVICE_ALL_APK/segway-delivery-debug-$VERSION_NAME.apk


#cp -f meituan/build/outputs/apk/release/meituan-web-release.apk $SERVICE_ALL_APK/meituan-web-release-unsigned.apk
#cp -f express/build/outputs/apk/release/segway-express-release.apk $SERVICE_ALL_APK/segway-express-release-unsigned.apk
cp -f daemon/build/outputs/apk/release/daemon-release-unsigned.apk $SERVICE_ALL_APK/daemon-release-unsigned.apk


TOOLS_FILE="/home/hdisk/user/mengpengfei/tools"

#$TOOLS_FILE/android-studio/jre/bin/java -jar $TOOLS_FILE/android-sdk-linux/build-tools/27.0.0/lib/apksigner.jar sign --ks /home/hdisk/user/mengpengfei/signed/android/my-release-key.jks --ks-pass pass:Ninebot@2018 -out $SERVICE_ALL_APK/meituan-web-release-signed-$VERSION_NAME.apk $SERVICE_ALL_APK/meituan-web-release-unsigned.apk
#$TOOLS_FILE/android-studio/jre/bin/java -jar $TOOLS_FILE/android-sdk-linux/build-tools/27.0.0/lib/apksigner.jar sign --ks /home/hdisk/user/mengpengfei/signed/android/my-release-key.jks --ks-pass pass:Ninebot@2018 -out $SERVICE_ALL_APK/segway-express-release-signed-$VERSION_NAME.apk $SERVICE_ALL_APK/segway-express-release-unsigned.apk
$TOOLS_FILE/android-studio/jre/bin/java -jar $TOOLS_FILE/android-sdk-linux/build-tools/27.0.0/lib/apksigner.jar sign --ks /home/hdisk/user/mengpengfei/signed/android/my-release-key.jks --ks-pass pass:Ninebot@2018 -out $SERVICE_ALL_APK/segway-delivery-debug-signed-$VERSION_NAME.apk $SERVICE_ALL_APK/segway-delivery-debug-$VERSION_NAME.apk

#$TOOLS_FILE/android-studio/jre/bin/java -jar $TOOLS_FILE/android-sdk-linux/build-tools/27.0.0/lib/apksigner.jar sign --ks /home/hdisk/user/mengpengfei/signed/android/my-release-key.jks --ks-pass pass:Ninebot@2018 -out $SERVICE_ALL_APK/launcher-release-signed-$VERSION_NAME.apk $SERVICE_ALL_APK/launcher-release-unsigned.apk

git tag $DATE

######EVT4.0#####
cd /home/hdisk/user/mengpengfei/signed/android/
java -jar signapk.jar platform.x509.pem platform.pk8 $SERVICE_ALL_APK/segway-delivery-debug-$VERSION_NAME.apk  $SERVICE_ALL_APK/segway-delivery-debug-signed-$VERSION_NAME.apk

java -jar signapk.jar platform.x509.pem platform.pk8 $SERVICE_ALL_APK/daemon-release-unsigned.apk  $SERVICE_ALL_APK/daemon-release-signed-$VERSION_NAME.apk




echo ${VERSION_NAME} > ${RELEASE_NOTES_PATH}/app-apr-food-deliver-meituan/version


cp $CODE_DIR/OTA_ReleaseNotes $SERVICE_ALL_APK/

#SEGWAY_LAUNCHER_PKG_NAME=`/home/hdisk/user/mengpengfei/tools/android-sdk-linux/build-tools/24.0.0/aapt dump badging  $SERVICE_ALL_APK/daemon-release-signed-$VERSION_NAME.apk |  grep  versionName  | awk '{printf $2}' | awk -F"'" '{print $2}'`
#SEGWAY_APP_PKG_NAME=`/home/hdisk/user/mengpengfei/tools/android-sdk-linux/build-tools/24.0.0/aapt dump badging  $SERVICE_ALL_APK/segway-app-debug-signed-$VERSION_NAME.apk |  grep  versionName  | awk '{printf $2}' | awk -F"'" '{print $2}'`

#SCOOTER_APP_PKG_NAME=`/home/hdisk/user/mengpengfei/tools/android-sdk-linux/build-tools/24.0.0/aapt dump badging  $SERVICE_ALL_APK/scooter_app-release-signed-$SCOOTER_APP_V.apk |  grep  versionName  | awk '{printf $2}' | awk -F"'" '{print $2}'`



#CURL_SEGWAY_LAUNCHER="\"package_name\":\"${SEGWAY_LAUNCHER_PKG_NAME}\",\"apk_version\":\"${VERSION_NAME}\""

#CURL_SEGWAY_APP="\"package_name\":\"${SEGWAY_APP_PKG_NAME}\",\"apk_version\":\"${VERSION_NAME}\""




#CURL_URL="http://120.92.20.57:3001/new_apk"



#scp $SERVICE_ALL_APK/daemon-release-signed-$VERSION_NAME.apk houwei@120.92.20.57:/home/houwei/GX/APP_TMP/Launcher-${VERSION_NAME}.apk
#REMOTE_CMD_LAUNCHER="/home/houwei/GX/shell/gx_app_mv_launcher.sh"
#ssh -t houwei@120.92.20.57 "${REMOTE_CMD_LAUNCHER}"

#scp $SERVICE_ALL_APK/segway-app-debug-signed-$VERSION_NAME.apk houwei@120.92.20.57:/home/houwei/GX/APP_TMP/SegwayDelivery-${VERSION_NAME}.apk
#REMOTE_CMD_DELIVERY="/home/houwei/GX/shell/gx_app_mv_segwaydelivery.sh"
#ssh -t houwei@120.92.20.57 "${REMOTE_CMD_DELIVERY}"





#RUN_COMMAND3=`echo "curl -X POST --header 'Content-Type:application/json' --header 'Accept:application/json' -d '{$CURL_SEGWAY_LAUNCHER}'  '${CURL_URL}'"`
#RUN_COMMAND6=`echo "curl -X POST --header 'Content-Type:application/json' --header 'Accept:application/json' -d '{$CURL_SEGWAY_APP}'  '${CURL_URL}'"`



#eval $RUN_COMMAND6


#CURL_RESULT=`eval $RUN_COMMAND | grep "successfully"`
#eval $RUN_COMMAND3 | grep "successfully"
#RUN_STATUS=`echo $?`

#if [ ! "${RUN_STATUS}" = "0" ];then
#        exit 1
#fi


#fi