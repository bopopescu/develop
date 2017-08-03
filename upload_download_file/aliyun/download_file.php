<?php
/**
* get_object_to_local_file
*
* @param OssClient $ossClient OSSClient实例
* @param string $bucket 存储空间名称
* @return null
*/

require_once __DIR__.'/aliyun/autoload.php';

use OSS\OssClient;
use OSS\Core\OssException;

$accessKeyId = "";
$accessKeySecret = "";
$endpoint = "";
$bucket = "";

function downloadFile($ossClient, $bucket)
{
    $object = "2017/07/20170706.zip";
    $localfile = "download.txt";
    $options = array(
         OssClient::OSS_FILE_DOWNLOAD => $localfile,
    );
    try{
        $ossClient->getObject($bucket, $object, $options);
    } catch(OssException $e) {
        printf(__FUNCTION__ . ": FAILED\n");
        printf($e->getMessage() . "\n");
        return;
    }
    print(__FUNCTION__ . ": OK, please check localfile: 'upload-test-object-name.txt'" . "\n");
}

$ossClient = new OssClient($accessKeyId, $accessKeySecret, $endpoint, false /* use cname */);
downloadFile($ossClient, $bucket);
?>
