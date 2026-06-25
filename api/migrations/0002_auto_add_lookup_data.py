from django.db import migrations

def create_lookup_data(apps, schema_editor):
    DonationType = apps.get_model('api', 'DonationType')
    FundraisingFrequency = apps.get_model('api', 'FundraisingFrequency')
    RequiredSubmissionType = apps.get_model('api', 'RequiredSubmissionType')
    ApplicationStatus = apps.get_model('api', 'ApplicationStatus')
    CommunicationType = apps.get_model('api', 'CommunicationType')
    Sector = apps.get_model('api', 'Sector')

    sectors = ['Health', 'Agriculture', 'Education', 'Environment', 'Technology']
    for s in sectors:
        Sector.objects.get_or_create(name=s)

    donation_types = ['Grant', 'Technical Support', 'Fellowship', 'CSR Donation', 'Loan']
    for dt in donation_types:
        DonationType.objects.get_or_create(name=dt)

    frequencies = ['Annual', 'Periodic', 'Rolling', 'Ongoing']
    for f in frequencies:
        FundraisingFrequency.objects.get_or_create(name=f)

    submission_types = ['Proposal', 'Bid', 'Pitch', 'Concept Note']
    for st in submission_types:
        RequiredSubmissionType.objects.get_or_create(name=st)

    statuses = ['Draft', 'Submitted', 'Under Review', 'Awarded', 'Rejected', 'Withdrawn']
    for st in statuses:
        ApplicationStatus.objects.get_or_create(name=st)

    comm_types = ['Email', 'Meeting', 'Phone Call', 'Video Call', 'Other']
    for ct in comm_types:
        CommunicationType.objects.get_or_create(name=ct)

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_lookup_data),
    ]