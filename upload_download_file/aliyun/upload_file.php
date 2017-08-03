<?php
/**
* 上传指定的本地文件内容
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
$localfile = "test.php";

function uploadFile($ossClient, $bucket, $localfile)
{
    $dir = date('Ymd')."/";
    $remotefile = $dir.md5(uniqid());
    try{
        $ossClient->uploadFile($bucket, $remotefile, $localfile);
       } 
    catch(OssException $e) {
        printf(__FUNCTION__ . ": FAILED\n");
        printf($e->getMessage() . "\n");
        return;
    }
    print(__FUNCTION__ . ": OK" . "\n");
}

$ossClient = new OssClient($accessKeyId, $accessKeySecret, $endpoint, false /* use cname */);
#uploadFile($ossClient, $bucket, $localfile);
function upload($localfile){
    Global $ossClient;
    Global $bucket;
    echo "localfile is ".$localfile."\n";
    uploadFile($ossClient, $bucket, $localfile);
}
?>
