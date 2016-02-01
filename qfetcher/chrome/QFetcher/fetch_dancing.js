
function tango(){

	// get group number
	var group_name = document.getElementsByClassName("group_name")[0].getElementsByTagName('a');
	var group_no = group_name[0].href.match(/\d+/g);
	//console.dir(group_no[0]);
	
	// get members
	var member_ids = document.getElementsByClassName("member_id");
	if(member_ids==null) return;
	var results = new Array();
	console.dir("member count: " + member_ids.length);
	for(i=0;i<member_ids.length;i++){
		numstr = member_ids[i].innerHTML;
		item = group_no[0] + ":" + numstr.substring(numstr.indexOf("(")+1, numstr.indexOf(")"));
		//console.dir(numstr + " - " + item + ", " + numstr.length + " - " + numstr.indexOf("(") + " - " + numstr.indexOf(")") );
		//console.log(item);
		results.push(cloneObject(item));
	}
	
	chrome.extension.sendRequest(results);	
}

function cloneObject(obj) {
    if (obj === null || typeof obj !== 'object') {
        return obj;
    }
 
    var temp = obj.constructor(); // give temp the original obj's constructor
    for (var key in obj) {
		console.dir(obj[key]);
        temp[key] = cloneObject(obj[key]);
    }
	
    return temp;
}
tango();
