function mouseOver(element) {
    element.classList.add("animate-change");
    element.classList.add("changed");
    element.classList.add("animated-fast");
}

function mouseOut(element) {
    element.classList.remove("animate-change");
    element.classList.remove("changed");
    element.classList.remove("animated-fast");
}

window.onunload = function(){ window.scrollTo(0,0); }

$("#module-container div").draggable({
    containment: '#example-container',
    stack: '#module-container div',
    cursor: 'move',
    revert: true
});

$("#drop-block").droppable({
    accept: '#module-container div',
    cursor: 'hovered',
    drop: handleDrop
});

var mod_no = 1
var image_name = ""
var module_names = ["face", "features", "age", "gender"]


function handleDrop(event, ui){
    var correct_module = "module-"+mod_no;
    var dragged_module = $(ui.draggable).attr("id"); 
    var module = ""

    var check = correct_module.localeCompare(dragged_module)

    if(correct_module == "module-3" && dragged_module == "module-4" || correct_module == "module-4" && dragged_module == "module-3"){
        check = 0
    }

    if(check == 0){
        
        //console.log("used-"+dragged_module);
        ui.draggable.position( { of: $("#used-"+dragged_module), my: 'left top', at: 'left top' } );
        ui.draggable.draggable( 'option', 'revert', false );
        module = module_names[dragged_module.match(/\d+/)[0] - 1]
        mod_no += 1
        
        $.ajax({
            type:"POST",
            url:"run_module/",
            data:{
                module: module,
                data: image_name
            },
            success: function(data){
                
                var timestamp = new Date().getTime();          
                var el = document.getElementById("image_output");          
                el.src = "/media/images/output/output_image.jpg?t=" + timestamp; 
                console.log(data)
            }
        })
    }
}

formdata = new FormData();

$("#image_to_upload").on("change", function(){
    var reader = new FileReader();
    var file = this.files[0];
		if (formdata) {
            formdata.append("title", "user_image");
			formdata.append("image", file);
			jQuery.ajax({
				url: "image_upload/",
				type: "POST",
				data: formdata,
				processData: false,
				contentType: false,
				success:function(data){
                    image_name = data.data
                    console.log(data);

                    // Preview the uploaded image
                    reader.onload = function (e) {
                        $('#image_preview').attr('src', e.target.result);
                    }
                    reader.readAsDataURL(file);
                },
                error: function(data){
                    console.log("error");
                    console.log(data);
                }
			});
        }
    	
});

function getRandomTweet(){
    $.ajax({
        method: "GET",
        url:"run_sentiment",
        dataType: "text",
        beforeSend: function(){
            $("#loader-1").show();
        },
        success: function(data){
            $("#loader-1").hide();
            console.log("All GOOD");
            $('#tweet-loc').html(data);
        },
        error: function(data){
            console.log("There was an error");
            console.log(data);
        }
    });
};

$("#sentiment-mod-container div").draggable({
    containment: '#example-container',
    stack: '#sentiment-mod-container div',
    cursor: 'move',
    revert: true
});

$("#sentiment-drop-block").droppable({
    accept: '#sentiment-mod-container div',
    cursor: 'hovered',
    drop: handleSentimentDrop
});

var mod_no = 1
var sentiment = "";
var tokenized, lemmatized, cleaned = [];
var ajaxFlag = false;
var response = [];

function handleSentimentDrop(event, ui){
    var correct_module = "module-"+mod_no;
    var dragged_module = $(ui.draggable).attr("id"); 

    var check = correct_module.localeCompare(dragged_module)

    if(check == 0){
        
        ui.draggable.position( { of: $("#used-"+dragged_module), my: 'left top', at: 'left top' } );
        ui.draggable.draggable( 'option', 'revert', false );
        if(!ajaxFlag){
            $.ajax({
                method: "POST",
                url:"run_sentiment/",
                async: false,
                data:{
                    tweet: $("#tweet-loc").val()
                },
                dataType: "json",
                success: function(data){
                    ajaxFlag = true;
                    tokenized = data.tokenized;
                    lemmatized = data.lemmatized;
                    cleaned = data.cleaned;
                    sentiment = data.sentiment;
                    console.log(ajaxFlag, "All GOOD");
                },
                error: function(data){
                    console.log("There was an error");
                    console.log(data);
                }
            });
        }
        if(mod_no == 1){
            response = tokenized;
        }
        else if(mod_no == 2){
            response = lemmatized;
        }
        else if(mod_no == 3){
            response = cleaned;
        }
        else{
            response = sentiment;
        }
        
        if(mod_no != 4){
            $('#list-holder').html("<ul id='newList' class='list-inline token'></ul>");
            for (cnt = 0; cnt < response.length; cnt++) {
                $("#newList").append("<li class='list-inline-item token'>"+response[cnt]+"</li>");
            }
        }
        else{
            if(sentiment == "Happy"){
                $("#sentiment-holder").html("<h3 class='text-success'>Sentiment: Happy &#128512;");
            }
            else{
                $("#sentiment-holder").html("<h3 class='text-danger'>Sentiment: Unhappy &#128542;");
            }
        }

        mod_no += 1;

    }
}

