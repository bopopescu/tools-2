// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

chrome.extension.onRequest.addListener(function(results) {
	qs = "";
	for (var i in results) {		
		qs += results[i] + ";";
	}
	
	//msg = "{\"no\":\"" + qs + "\"}";
	msg = "no=" + qs;
	post_msg(msg);
	document.getElementById("result_table").innerHTML = "<h3>QQ count: " + results.length + "</h3>";
	document.getElementById("post_status").innerHTML = "<h4>Wait...</h4>";	
});

// Set up event handlers and inject send_links.js into all frames in the active
// tab.
window.onload = function() {
	chrome.windows.getCurrent(function (currentWindow) {
		chrome.tabs.query({active: true, windowId: currentWindow.id},
						  function(activeTabs) {
		  chrome.tabs.executeScript(
			activeTabs[0].id, {file: 'fetch_dancing.js', allFrames: true});
		});
	});
};

function post_msg(msg)
{
	$.post(
		"http://liudonghua.net/qqnum/report.php",
		msg
	).done(function(data){
		console.dir(data);
		document.getElementById("post_status").innerHTML = "<h4>OK: " + data + "</h4>";
	});
}

