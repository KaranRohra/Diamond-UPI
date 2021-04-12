function alert_box(id) {
    var box = confirm("Sure you want to reject request?")
    if(box){
        window.location.replace("/accept_or_reject/reject/?id="+id)
    }
}