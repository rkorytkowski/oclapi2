from django.core.exceptions import ValidationError
from django.db import models, IntegrityError, transaction
from pydash import get, compact

from core.common.constants import TEMP
from core.common.mixins import SourceChildMixin
from core.common.models import VersionedModel
from core.mappings.constants import MAPPING_TYPE, MAPPING_IS_ALREADY_RETIRED, MAPPING_WAS_RETIRED, \
    MAPPING_IS_ALREADY_NOT_RETIRED, MAPPING_WAS_UNRETIRED
from core.mappings.mixins import MappingValidationMixin


class Mapping(MappingValidationMixin, SourceChildMixin, VersionedModel):
    class Meta:
        db_table = 'mappings'

    parent = models.ForeignKey('sources.Source', related_name='mappings_set', on_delete=models.DO_NOTHING)
    map_type = models.TextField()
    from_concept = models.ForeignKey(
        'concepts.Concept', related_name='mappings_from', on_delete=models.CASCADE
    )
    to_concept = models.ForeignKey(
        'concepts.Concept', null=True, blank=True, related_name='mappings_to', on_delete=models.CASCADE
    )
    to_source = models.ForeignKey(
        'sources.Source', null=True, blank=True, related_name='mappings_to', on_delete=models.CASCADE
    )
    to_concept_code = models.TextField(null=True, blank=True)
    to_concept_name = models.TextField(null=True, blank=True)
    sources = models.ManyToManyField('sources.Source', related_name='mappings')
    external_id = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    versioned_object_id = models.BigIntegerField(null=True, blank=True)
    name = None
    full_name = None
    default_locale = None
    supported_locales = None
    website = None
    description = None
    mnemonic = None
    mnemonic_attr = 'versioned_object_id'

    OBJECT_TYPE = MAPPING_TYPE

    @property
    def mnemonic(self):  # pylint: disable=function-redefined
        return self.versioned_object_id

    @property
    def mapping(self):  # for url kwargs
        return self.mnemonic

    @property
    def source(self):
        return get(self, 'parent.mnemonic')

    @property
    def parent_source(self):
        return self.parent

    @property
    def from_source(self):
        return self.from_concept.parent

    @property
    def from_source_owner(self):
        return self.from_source.owner_name

    @property
    def from_source_owner_mnemonic(self):
        return self.from_source.owner.mnemonic

    @property
    def from_source_owner_type(self):
        return self.from_source.owner_type

    @property
    def from_source_name(self):
        return self.from_source.mnemonic

    @property
    def from_source_url(self):
        return self.from_source.url

    @property
    def from_source_shorthand(self):
        return "%s:%s" % (self.from_source_owner_mnemonic, self.from_source_name)

    @property
    def from_concept_code(self):
        return self.from_concept.mnemonic

    @property
    def from_concept_name(self):
        return self.from_concept.display_name

    @property
    def from_concept_url(self):
        return self.from_concept.url

    @property
    def from_concept_shorthand(self):
        return "%s:%s" % (self.from_source_shorthand, self.from_concept_code)

    def get_to_source(self):
        if self.to_source_id:
            return self.to_source
        if self.to_concept_id:
            return self.to_concept.parent

        return None

    @property
    def to_source_name(self):
        return get(self.get_to_source(), 'mnemonic')

    @property
    def to_source_url(self):
        return get(self.get_to_source(), 'url')

    @property
    def to_source_owner(self):
        return str(get(self.get_to_source(), 'parent', ''))

    @property
    def to_source_owner_mnemonic(self):
        return get(self.get_to_source(), 'owner.mnemonic')

    @property
    def to_source_owner_type(self):
        return get(self.get_to_source(), 'owner_type')

    @property
    def to_source_shorthand(self):
        return self.get_to_source() and "%s:%s" % (self.to_source_owner_mnemonic, self.to_source_name)

    def get_to_concept_name(self):
        if self.to_concept_name:
            return self.to_concept_name

        if self.to_concept_id:
            return self.to_concept.display_name

        return None

    def get_to_concept_code(self):
        return self.to_concept_code or (self.to_concept and self.to_concept.mnemonic)

    @property
    def to_concept_url(self):
        return self.to_concept.url if self.to_concept else None

    @property
    def to_concept_shorthand(self):
        return "%s:%s" % (self.to_source_shorthand, self.get_to_concept_code)

    @staticmethod
    def get_resource_url_kwarg():
        return 'mapping'

    @staticmethod
    def get_version_url_kwarg():
        return 'mapping_version'

    def clone(self, user=None):
        return Mapping(
            version=TEMP,
            parent_id=self.parent_id,
            map_type=self.map_type,
            from_concept_id=self.from_concept_id,
            to_concept_id=self.to_concept_id,
            to_source_id=self.to_source_id,
            to_concept_code=self.to_concept_code,
            to_concept_name=self.to_concept_name,
            retired=self.retired,
            released=self.released,
            is_latest_version=self.is_latest_version,
            extras=self.extras,
            created_by=user,
            updated_by=user,
            public_access=self.public_access,
            external_id=self.external_id,
            versioned_object_id=self.versioned_object_id
        )

    @classmethod
    def persist_new(cls, data, user):
        mapping = Mapping(**data, created_by=user, updated_by=user)

        mapping.version = TEMP
        mapping.errors = dict()

        try:
            mapping.full_clean()
            mapping.save()
            mapping.version = str(mapping.id)
            mapping.versioned_object_id = mapping.id
            mapping.save()
            parent = mapping.parent
            parent_head = parent.head
            mapping.sources.set([parent, parent.head])
            parent.save()
            parent_head.save()
        except ValidationError as ex:
            mapping.errors.update(ex.message_dict)
        except IntegrityError as ex:
            mapping.errors.update(dict(__all__=ex.args))

        return mapping

    @classmethod
    @transaction.atomic
    def persist_clone(cls, obj, user=None, **kwargs):
        errors = dict()
        if not user:
            errors['version_created_by'] = "Must specify which user is attempting to create a new {} version.".format(
                cls.get_resource_url_kwarg()
            )
            return errors
        obj.version = TEMP
        obj.created_by = user
        parent = obj.parent
        parent_head = parent.head
        persisted = False
        errored_action = 'saving new mapping version'
        latest_versions = None
        try:
            obj.is_latest_version = True
            obj.full_clean()
            obj.save(**kwargs)
            obj.version = str(obj.id)
            obj.save()
            latest_versions = obj.versions.exclude(id=obj.id).filter(is_latest_version=True)
            latest_versions.update(is_latest_version=False)
            obj.sources.set(compact([parent, parent_head]))

            # to update counts
            parent.save()
            parent_head.save()

            persisted = True
        except ValidationError as err:
            errors.update(err.message_dict)
        finally:
            if not persisted:
                obj.sources.remove(parent_head)
                if latest_versions:
                    latest_versions.update(is_latest_version=True)
                if obj.id:
                    obj.delete()
                errors['non_field_errors'] = ['An error occurred while %s.' % errored_action]

        return errors

    def retire(self, user, comment=None):
        if self.head.retired:
            return {'__all__': MAPPING_IS_ALREADY_RETIRED}

        return self.__update_retire(True, comment or MAPPING_WAS_RETIRED, user)

    def unretire(self, user, comment=None):
        if not self.head.retired:
            return {'__all__': MAPPING_IS_ALREADY_NOT_RETIRED}

        return self.__update_retire(False, comment or MAPPING_WAS_UNRETIRED, user)
