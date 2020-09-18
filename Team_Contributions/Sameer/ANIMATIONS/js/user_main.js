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
})

$("#drop-block").droppable({
    accept: '#module-container div',
    cursor: 'hovered',
    drop: handleDrop
})

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
    	
})