from django.core.exceptions import ValidationError
from mock import patch, Mock

from core.common.constants import ACCESS_TYPE_NONE, HEAD
from core.common.tests import OCLTestCase
from core.orgs.constants import ORG_OBJECT_TYPE
from core.orgs.models import Organization
from core.orgs.tests.factories import OrganizationFactory


class OrganizationTest(OCLTestCase):
    def test_resource_type(self):
        self.assertEqual(Organization().resource_type(), ORG_OBJECT_TYPE)

    def test_org(self):
        self.assertEqual(Organization().org, '')
        self.assertEqual(Organization(mnemonic='blah').org, 'blah')

    def test_members(self):
        org = Organization(id=123)
        self.assertEqual(org.members.count(), 0)

    def test_create_organization_negative__no_name(self):
        with self.assertRaises(ValidationError):
            org = Organization(mnemonic='org1')
            org.full_clean()
            org.save()

    def test_create_organization_negative__no_mnemonic(self):
        with self.assertRaises(ValidationError):
            org = Organization(name='My Organization')
            org.full_clean()
            org.save()

    def test_organization_delete(self):
        org = OrganizationFactory()
        org_id = org.id

        self.assertTrue(org.is_active)
        self.assertTrue(Organization.objects.filter(id=org_id).exists())
        org.soft_delete()
        self.assertFalse(org.is_active)
        self.assertTrue(Organization.objects.filter(id=org_id).exists())
        org.delete()
        self.assertFalse(Organization.objects.filter(id=org_id).exists())

    @patch('core.orgs.models.Organization.source_set')
    def test_public_sources(self, source_set_mock):
        source_set_mock.exclude = Mock(return_value=Mock(filter=Mock(return_value=Mock(count=Mock(return_value=10)))))

        self.assertEqual(Organization().public_sources, 10)
        source_set_mock.exclude.assert_called_once_with(public_access=ACCESS_TYPE_NONE)
        source_set_mock.exclude().filter.assert_called_once_with(version=HEAD)
        source_set_mock.exclude().filter().count.assert_called_once()

    def test_create_org_special_characters(self):
        # period in mnemonic
        org = OrganizationFactory(name='test', mnemonic='org.1')
        self.assertTrue(org.id)
        self.assertEquals(org.mnemonic, 'org.1')

        # hyphen in mnemonic
        org = OrganizationFactory(name='test', mnemonic='org-1')
        self.assertTrue(org.id)
        self.assertEquals(org.mnemonic, 'org-1')

        # underscore in mnemonic
        org = OrganizationFactory(name='test', mnemonic='org_1')
        self.assertTrue(org.id)
        self.assertEquals(org.mnemonic, 'org_1')

        # all characters in mnemonic
        org = OrganizationFactory(name='test', mnemonic='org.1_2-3')
        self.assertTrue(org.id)
        self.assertEquals(org.mnemonic, 'org.1_2-3')

        # @ characters in mnemonic
        org = OrganizationFactory(name='test', mnemonic='org@1')
        self.assertTrue(org.id)
        self.assertEquals(org.mnemonic, 'org@1')
