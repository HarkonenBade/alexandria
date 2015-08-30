var renderer = new marked.Renderer();

renderer.image = function (href, title, text) {
    return '<img class="img-responsive" src="' + href + '" alt="' + text + '" title="' + title + '" />';
}


jQuery(document).ready(function() {
    jQuery("time.timeago").timeago();

    $(".quote-text").each(function(index, current){
        current.innerHTML = marked(current.innerHTML, {renderer: renderer});
    });
});
