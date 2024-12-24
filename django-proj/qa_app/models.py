# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from pgvector.django import VectorField


class LangchainPgCollection(models.Model):
    name = models.CharField(blank=True, null=True)
    cmetadata = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    uuid = models.UUIDField(primary_key=True)

    class Meta:
        managed = False
        db_table = "langchain_pg_collection"


class LangchainPgEmbedding(models.Model):
    collection = models.ForeignKey(
        LangchainPgCollection, models.DO_NOTHING, blank=True, null=True
    )
    embedding = VectorField(dimensions=1536)
    document = models.CharField(blank=True, null=True)
    cmetadata = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    custom_id = models.CharField(blank=True, null=True)
    uuid = models.UUIDField(primary_key=True)

    class Meta:
        managed = False
        db_table = "langchain_pg_embedding"
