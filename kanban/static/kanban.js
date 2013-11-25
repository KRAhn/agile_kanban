/**
 * Created by acuros_ on 13. 11. 25..
 */

$(function()
{
    $.get('/iteration/now/', function(data){
        console.log(data)
    },  'json');
});