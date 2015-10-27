$.fn.firstWord = function() {
  str = this.html().replace(/<p>(\S+)/, "<span class='firstWord'>$1</span>");
  this.html(str);
};

$( window ).load(function() {
    $("#firstWord").firstWord();
});
