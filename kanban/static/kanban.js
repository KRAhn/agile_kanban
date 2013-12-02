/**
 * Created by acuros_ on 13. 11. 25..
 */

var TaskManager = {
  initialize: function() {
    this.$taskSection = $('#tasks');
  },
  taskGroups: [],
  renderPage: function () {
    this.taskGroups.forEach(function (taskGroup) {
      this.$taskSection.append(taskGroup.$element);
    }, this);
    $('.task-list').sortable({
      connectWith: ".task-list",
      cursor: "move"
    }).disableSelection();
    $('.task-list').on('sortupdate', $.proxy(function(event, ui){
      if(ui.sender != undefined) {
        var from = this.getTaskGroupWithName(ui.sender.attr('data-name'));
        var to = this.getTaskGroupWithName($(event.currentTarget).attr('data-name'));
        var taskId = ui.item.children('article').attr('data-id');
        from.tasks.forEach(function(task) {
          if(task.id == taskId)
            ui.item.task = task;
        });
        from.tasks = from.tasks.filter(function(task){return task.id != taskId;})
        to.tasks.push(ui.item.task);
        ui.item.task.status = to.name;
        ui.item.task.push();
      }
    }, this));
  },
  getTaskGroupWithName: function(name) {
    for(var i=0; i<this.taskGroups.length; ++i) {
      if(this.taskGroups[i].name == name)
        return this.taskGroups[i];
    }
    return null;
  }
};

var TaskGroup = function(id, name, displayName, tasks) {
  if(!(this instanceof TaskGroup)) {
    return new TaskGroup(id, name, displayName, tasks);
  }
  this.id = id;
  this.name = name;
  this.displayName = displayName;
  this.tasks = tasks.map(function(task) {
    return new Task(task.id, task.title, task.description, task.author, task.status, task.createdTime);
  });

  this.$element = this.render();
  this.emptyCard = new EmptyCard(this);
};

TaskGroup.prototype.render = function () {
  var $section = $('<section class="task-group"></section>');
  $section.attr('id', this.name);

  var $title = $('<h1></h1>');
  $title.text(this.displayName);
  $section.append($title);

  var $taskList = $('<ul class="task-list"></ul>');
  $taskList.attr('id', this.name + '-list');
  $taskList.attr('data-name', this.name);
  $section.append($taskList);

  this.tasks.forEach(function (task) {
    var $li = $('<li></li>');
    $li.append(task.render());
    $taskList.append($li);
  });

  var $addButton = $('<button class="add-card">Add card</button>');
  $addButton.on('click', $.proxy(this.onAddCardClicked, this));
  $section.append($addButton);

  return $section;
};

TaskGroup.prototype.onAddCardClicked = function(e) {
  $(e.currentTarget).hide();
  this.emptyCard.$element.show();
};

TaskGroup.prototype.addTask = function(task) {
  this.tasks.push(task);
  var $li = $('<li></li>');
  $li.append(task.render());
  this.$element.children('task-list').append($li);
}



var Task = function(id, title, description, author, status, createdTime) {
  if(!(this instanceof Task)) {
    return new Task(id, title, description, author, status, createdTime);
  }
  this.id = id;
  this.title = title;
  this.description = description;
  this.author = author;
  this.status = status;
  this.createdTime = createdTime;

  this.$element = undefined;
};

Task.prototype.render = function() {
  var $article = $('<article class="task"></article>');
  $article.attr('data-id', this.id);

  var $header = $('<header></header>');
  var $title = $('<h1></h1>');
  $title.text(this.title);
  $header.append($title);
  $header.append($(document.createTextNode(this.author + ' , ' + this.createdTime)));

  $article.append($header);
  $article.append($('<p>'+this.description+'</p>'));
  return $article;
};

Task.prototype.push = function() {
  $.post('/task/'+this.id+'/edit/', {
    title:this.title,
    description:this.description,
    author:this.author,
    status:this.status
  }, function(data){
    console.log(data);
  }, 'json');
}




var EmptyCard = function(taskGroup){
  if(!(this instanceof EmptyCard)){
    return new EmptyCard(taskGroup);
  }

  this.taskGroup = taskGroup;
  this.$element = $('\
  <form action="/iteration/now/add/" method="post" class="empty-card task">\
    <table>\
      <tr>\
        <td><label for="new-title">제목</label></td>\
        <td><input type="text" id="new-title" /></td>\
      </tr>\
      <tr>\
        <td><label for="new-author">작성자</label></td>\
        <td><input type="text" id="new-author" /></td>\
      </tr>\
      <tr>\
        <td><label for="new-description">설명</label></td>\
        <td><textarea id="new-description"></textarea></td>\
      </tr>\
    </table>\
    <input type="submit" value="저장" /><br />\
    <input type="reset" value="취소" />\
  </form>');
  this.taskGroup.$element.append(this.$element);
  this.taskGroup.$element.on('submit', '.empty-card', $.proxy(this.onSubmit, this));
  this.taskGroup.$element.on('reset', '.empty-card', $.proxy(function() {
    this.$element.hide();
    this.taskGroup.$element.find('.add-card').show();
    return false;
  }, this));
};

EmptyCard.prototype.onSubmit = function(e) {
  e.preventDefault();

  var title = this.$element.find('#new-title').val();
  var author= this.$element.find('#new-author').val();
  var description = this.$element.find('#new-description').val();
  var now = new Date();
  var createdTime = $.datepicker.formatDate('yy-mm-dd', now) + ' ' +
                    [now.getHours(), now.getMinutes(), now.getSeconds()].join(':');
  var status = this.taskGroup.name;
  var task = new Task(title, description, author, status, createdTime);
  this.taskGroup.tasks.push(task);;
  this.taskGroup.$element.addTask(task);

  this.$element.hide();
  this.$element.find('input[type="text"], textarea').each(function()
  {
    $(this).val('');
  });
  this.taskGroup.$element.find('.add-card').show();

  this.submit(task);
};

EmptyCard.prototype.submit = function (task) {
  $.post(this.$element.attr('action'),
         {
           title: task.title,
           description: task.description,
           author: task.author,
           status_name: task.status,
           created_time: task.createdTime
         },
        function(data){
          console.log(data);
        }
  );
};




$(function()
{
  TaskManager.initialize();
  $.get('/iteration/now/', function(iteration){
    $('#iteration-goal').text(iteration.goal);
    TaskManager.taskGroups = iteration.taskGroups.map(function(taskGroup){
      return new TaskGroup(taskGroup.id,
                           taskGroup.name,
                           taskGroup.displayName,
                           taskGroup.tasks);
    });

    TaskManager.renderPage();
  },  'json');

});