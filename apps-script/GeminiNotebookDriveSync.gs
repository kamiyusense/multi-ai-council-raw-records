const MAX_BUNDLE_CHARS = 5 * 1024 * 1024;

function doPost(event) {
  const properties = PropertiesService.getScriptProperties();
  const expectedToken = properties.getProperty('SYNC_TOKEN');
  const driveFileId = properties.getProperty('DRIVE_FILE_ID');
  const suppliedToken = event && event.parameter && event.parameter.token;
  const content = event && event.postData && event.postData.contents;

  if (!expectedToken || !driveFileId) return jsonResponse({ok: false, error: 'server_not_configured'});
  if (!suppliedToken || !constantTimeEquals(suppliedToken, expectedToken)) return jsonResponse({ok: false, error: 'unauthorized'});
  if (typeof content !== 'string' || content.length === 0 || content.length > MAX_BUNDLE_CHARS) return jsonResponse({ok: false, error: 'invalid_content'});

  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(30 * 1000);
    DriveApp.getFileById(driveFileId).setContent(content);
    return jsonResponse({ok: true, bytes: Utilities.newBlob(content).getBytes().length});
  } catch (error) {
    console.error('Drive bundle sync failed: ' + error.message);
    return jsonResponse({ok: false, error: 'sync_failed'});
  } finally {
    if (lock.hasLock()) lock.releaseLock();
  }
}

function jsonResponse(value) {
  return ContentService.createTextOutput(JSON.stringify(value)).setMimeType(ContentService.MimeType.JSON);
}

function constantTimeEquals(left, right) {
  const leftBytes = Utilities.newBlob(left).getBytes();
  const rightBytes = Utilities.newBlob(right).getBytes();
  let difference = leftBytes.length ^ rightBytes.length;
  const length = Math.max(leftBytes.length, rightBytes.length);
  for (let index = 0; index < length; index += 1) difference |= (leftBytes[index] || 0) ^ (rightBytes[index] || 0);
  return difference === 0;
}
