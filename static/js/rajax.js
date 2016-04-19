/**
 * Created by kaishunsuke on 2016/03/07.
 */

$(window).load(init());

function init() {
  $("#y_button").click(function() {
    $("#y_button").prop("disabled", true);
    var input_data = $("#y_value").val();

    if (input_data.match(/^([1-9]\d*|0)(\.\d+)?$/)==null){
      alert("valid input!!")
      $("#y_button").prop("disabled", false);
        $("#y_value").val("")
        return false;

    }
    var ydata = JSON.stringify({"y":input_data});
    //loading
    dispLoading();

    $.ajax({
      type:'POST',
      url:'/ypost',
      data:ydata,
      contentType:'application/json',

      success:function(data) {
        //get data

        var result = JSON.parse(data.ResultSet);
        $("#hello").text(result);

        //button 復活
        $("#y_button").prop("disabled", false);
        $("#y_value").val("")
        $("#loading").removeClass("is-active")
        console.log(result["new_x"])
        //dom 追加
        add_li_dom(result["result_x"]);
        $("#new_x_span").text(result["new_x"]);
      },
      error: function(data){
        alert("error")
        $("#y_button").prop("disabled", false);
        $("#y_value").val("");
        $("#loading").removeClass("is-active");
        return false;
      }



    });

    return false;

  });




}









function dispLoading(){
    // 画面表示メッセージ
    $("#loading").addClass("is-active")

}

function add_li_dom(msg){

  //find last step num
  var ul = $("#result_list").children();
  if (ul.length == "0"){
    num = 1;
    console.log(num)
  }else{
    num = ul.length + 1
    console.log(num)
  }


  var li = $("<li></li>", {
    "class": "mdl-list__item",
    addClass: "li_size",
  });

  var span1 = $("<span></span>",{
    "class":"step",
    "text":"["+num+"]"
  });

  var span2 = $("<span></span>",{
    "class":"mdl-list__item-primary-content",
    "text":msg
  });




  li.append(span1);
  li.append(span2);

  $("#result_list").append(li);

}








var dialog = document.querySelector('dialog');
var showModalButton = document.querySelector('.show-modal');
if (! dialog.showModal) {
  dialogPolyfill.registerDialog(dialog);
}
showModalButton.addEventListener('click', function() {
  dialog.showModal();
});
dialog.querySelector('.close').addEventListener('click', function() {
  dialog.close();
});
