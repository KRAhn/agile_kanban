# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AccessLog'
        db.create_table(u'asap_web_accesslog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trace_key', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('query_string', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('referer', self.gf('django.db.models.fields.TextField')()),
            ('log_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'asap_web', ['AccessLog'])


    def backwards(self, orm):
        # Deleting model 'AccessLog'
        db.delete_table(u'asap_web_accesslog')


    models = {
        u'asap_web.accesslog': {
            'Meta': {'object_name': 'AccessLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'log_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'query_string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'referer': ('django.db.models.fields.TextField', [], {}),
            'trace_key': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        }
    }

    complete_apps = ['asap_web']