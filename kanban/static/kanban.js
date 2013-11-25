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
      taskGroup.$element = taskGroup.render();
      this.$taskSection.append(taskGroup.$element);
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
  this.$element = undefined;
  this.tasks = tasks.map(function(task) {
    new Task(task.title, task.description, task.author, task.status, task.createdTime);
  });

};

TaskGroup.prototype.render = function () {
  var $section = $('<section class="task-group"></section>');
  $section.attr('id', this.name);

  var $title = $('<h1></h1>');
  $title.text(this.displayName);
  $section.append($title);

  var $div = $('<div class="tasks-wrap"></div>');
  $section.append($div);

  this.tasks.forEach(function (task) {
    $div.append(task.render());
  });

  var $addButton = $('<button class="add-card">Add card</button>');
  $addButton.on('click', $.proxy(this.addCard, this));
  $section.append($addButton)

  return $section;
};

TaskGroup.prototype.addCard = function() {
  this.$element.children('.tasks-wrap').append(new EmptyCard(this).$element);
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

  this.$element = undefined;
};

Task.prototype.render = function() {
  var $article = $('<article class="task"></article>');

  var $header = $('<header></header>');
  var $title = $('<h1></h1>');
  $title.text(this.title);
  $header.append($title);
  $header.append($(this.author + ' , ' + this.createdTime));

  $article.append($header);
  return $article;
}

var EmptyCard = function(taskGroup){
  if(!(this instanceof EmptyCard)){
    return new EmptyCard(taskGroup);
  }

  this.taskGroup = taskGroup;
  this.$element = $('\
  <form method="post" class="empty-card task">\
    <table>\
      <tr>\
        <td><label for="new-title">제목</label></td>\
        <td><input type="text" id="new-title" /></td>\
      </tr>\
      <tr>\
        <td><label for="new-writer">작성자</label></td>\
        <td><input type="text" id="new-writer" /></td>\
      </tr>\
      <tr>\
        <td><label for="new-description">설명</label></td>\
        <td><textarea id="new-description"></textarea></td>\
      </tr>\
    </table>\
    <input type="submit" value="저장" /><br />\
    <input type="reset" value="취소" />\
  </form>');
  taskGroup.$element.on('submit', '.empty-card', function() {
    return false;
  });
  taskGroup.$element.on('reset', '.empty-card', $.proxy(function() {
    this.$element.remove();
    return false;
  }, this));

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