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
      this.$taskSection.append(taskGroup.render());
    }, this);
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
    new Task(task.title, task.description, task.author, task.status, task.createdTime);
  });

  this.render = function() {
    var $section = $('<section></section>');
    $section.attr('id', this.name);
    $section.addClass('task-group');

    var $head = $('<h1></h1>');
    $head.text(this.displayName);
    $section.append($head);

    this.tasks.forEach(function(task) {
      $section.append(task.render());
    });
    return $section;
  }
};

var Task = function(title, description, author, status, createdTime) {
  if(!(this instanceof Task)) {
    return new Task(title, description, author, status, createdTime);
  }

  this.title = title;
  this.description = description;
  this.author = author;
  this.status = status;
  this.createdTime = createdTime;

  this.render = function() {
    return '';
  }
};

$(function()
{
  TaskManager.initialize();
  $.get('/iteration/now/', function(taskGroups){
    TaskManager.taskGroups = taskGroups.map(function(taskGroup){
      return new TaskGroup(taskGroup.id,
                           taskGroup.name,
                           taskGroup.displayName,
                           taskGroup.tasks);
    });
    TaskManager.renderPage();
  },  'json');
});