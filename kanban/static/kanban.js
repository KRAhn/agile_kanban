/**
 * Created by acuros_ on 13. 11. 25..
 */

$(function()
{

    var TaskManager = {
        tasks : {},
        $taskSection : $('#tasks'),

        render : function() {
            this.$taskSection.empty();
            for(var id in this.tasks) {
                var $section = $('<section id="'+id+'"></section>');
                var $head = $('<h1>'+this.tasks[id].displayName+'</h1>');
                $section.append($head);
                for(var task in this.tasks[id]){
                    var $article = $();
                    $section.append();
                }
                this.$taskSection.append($section);
            }
        }
    };

    $.get('/iteration/now/', function(data){
        TaskManager.tasks = data;
        TaskManager.render();
    },  'json');
});