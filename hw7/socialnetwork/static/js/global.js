var max_date = "1970-01-01T00:00+00:00";
var max_pk = 0;

function getInitTime(){
    // console.log(max_date);
    $.ajax({
        url: "/socialnetwork/get-list-json/"+max_date,
        dataType: "json",
        success : updateInitTime
    });
}

function updateInitTime(posts){
    if($(posts).length) {
        max_date = posts[posts.length - 1].fields.creation_time;
    }
}


function getUpdate(){
    // console.log(max_date);
    $.ajax({
        url: "/socialnetwork/get-list-json/"+max_date,
        dataType: "json",
        success : updateList
    });
}

function updateList(posts){
    if($(posts).length){

        $(posts).each(function() {
        if (this.fields.creation_time!=max_date)
        {
            var comment_id = "'comment-button-"+this.pk+"-"+$("#follower-username").val()+"'";
            console.log("username: " +$("#follower-username").val());
              $("#post-list").prepend(
            "<div class=\"post\" id=\""+this.pk+"\">"+
            "    <a class=\"media-heading\" href=\"/socialnetwork/profile/"+ this.fields.created_by[0]+ " \">\n" +
            "       <img class=\"usr-img\" src=\"/socialnetwork/photo/"+this.fields.created_by[0]+"\"" +
            "           onerror=\"this.src='/static/images/blank-profile-picture.png'\" >\n" +
            "    </a>\n" +
            "    <p >Post by "+this.fields.created_by[0]+"</p>\n" +
            "    <p>"+this.fields.text+" </p>\n" +
            "    <div class=\"post-info\">\n" +
            "        "+ this.fields.creation_time+"\n" +
            "    </div>"+

            "   <div id=\"comment-list"+this.pk+"\"></div>"+
            "   <div class=\"comment\">\n" +
            "       <p>Comment:</p>\n" +
            "       <textarea id='comment-field"+this.pk+"' rows=\"2\" cols=\"100\" placeholder=\"Leave a comment here...\"></textarea>\n" +
            "       <button id = "+comment_id+" type=\"submit\" onclick=\"addComment("+comment_id+")\">Comment</button>\n" +
            "       <div class=\"error\" id='error\"+this.pk+\"'></div>\n" +
            "   </div>"+
            " </div>"
            );
        }

    });
    max_date = posts[posts.length - 1].fields.creation_time;
    }

    // console.log($('#post-list').children());
    $('#post-list').children().each(function(){
        getComments(this.id);
        // console.log("getcommet for post "+ this.id);
    });


}

function getComments(post_id){
    max_pk = 0
    var comments = $('#comment-list'+post_id).children();

    if(comments.length)
    {
        max_pk = parseInt(comments.last().attr("id").replace("comment-",''));
        // console.log("max_pk)"+max_pk);
    }

    $.ajax({
        url: "/socialnetwork/get-comments-changes/"+ max_pk +"/" + post_id,
        dataType: "json",
        success : updateComments
    });

}

function updateComments(comments){
    $(comments).each(function() {
        // console.log("this.fields.post: " +this.fields.post);
        // console.log($('#comment-list'+this.fields.post).children().length);
        $('#comment-list'+this.fields.post).append(
                "<div id=\"comment-"+ this.pk +"\" class=\"comment-text\">\n" +
                "                <br/>\n" +
                "                <p>Comment by\n" +
                "                    <a href=\"/socialnetwork/profile/"+ this.fields.created_by[0]+ " \">" +this.fields.created_by+"</a>\n" +
                "                    ---"+this.fields.content+"\n" +
                "                </p>\n" +
                "                <p>"+this.fields.created_time+"</p>\n" +
                "            </div>"
            );

    });
}

function addComment(post_id){
    // console.log(post_id);
    var tmp = post_id.split("-")
    post_id = tmp[2];
    var username = tmp[3];
    var commentText = $("#comment-field"+post_id).val();
    if(commentText == '' || post_id=='')
    {
        $("#error"+post_id).html("Invalid input! Leave some comment here...");
    }

    else{
        $.ajax({
         url: "/socialnetwork/add-comment/"+post_id,
         type:"POST",
         data:"text="+commentText+"&username="+username+"&csrfmiddlewaretoken="+getCSRFToken(),
         dataType: "json",
         success : redirect
    });
    }
}

function redirect(data){
    getUpdate();
}


function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}

// The global.html does not have the current updated time, so we call getInitTime()
// as soon as page is finished loading
 window.onload = getInitTime;

// causes list to be re-fetched every 5 seconds
window.setInterval(getUpdate, 5000);
