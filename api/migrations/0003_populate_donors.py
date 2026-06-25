# api/migrations/0003_populate_donors.py

from django.db import migrations
import re

def create_choices(apps, schema_editor):
    # Get models
    Sector = apps.get_model('api', 'Sector')
    DonationType = apps.get_model('api', 'DonationType')
    FundraisingFrequency = apps.get_model('api', 'FundraisingFrequency')
    RequiredSubmissionType = apps.get_model('api', 'RequiredSubmissionType')
    Tag = apps.get_model('api', 'Tag')
    Donor = apps.get_model('api', 'Donor')

    # --- Helper to get or create choices ---
    def get_or_create_sector(name):
        sector, _ = Sector.objects.get_or_create(name=name)
        return sector

    def get_or_create_donation_type(name):
        donation_type, _ = DonationType.objects.get_or_create(name=name)
        return donation_type

    def get_or_create_frequency(name):
        frequency, _ = FundraisingFrequency.objects.get_or_create(name=name)
        return frequency

    def get_or_create_submission_type(name):
        submission_type, _ = RequiredSubmissionType.objects.get_or_create(name=name)
        return submission_type

    def get_or_create_tag(name, sector=None):
        tag, _ = Tag.objects.get_or_create(name=name, defaults={'sector': sector})
        return tag

    # --- Helper to create a donor ---
    def create_donor(data):
        # Get or create sector(s)
        sectors = []
        for sector_name in data.get('sectors', []):
            sectors.append(get_or_create_sector(sector_name))

        donation_type = get_or_create_donation_type(data['donation_type'])
        frequency = get_or_create_frequency(data['fundraising_frequency'])
        submission_type = get_or_create_submission_type(data['what_is_required'])

        # Create donor
        donor, created = Donor.objects.get_or_create(
            name=data['name'],
            defaults={
                'donation_type': donation_type,
                'fundraising_frequency': frequency,
                'what_is_required': submission_type,
                'website': data.get('website', ''),
                'donor_relationship_strategy': data.get('donor_relationship_strategy', ''),
                'contact_person': data.get('contact_person', ''),
                'contact_email': data.get('contact_email', ''),
                'contact_phone': data.get('contact_phone', ''),
                'notes': data.get('notes', ''),
                'is_active': True,
            }
        )

        # Add sectors (ManyToMany)
        for sector in sectors:
            donor.sectors.add(sector)

        # Add specialisations (Tags)
        for tag_name in data.get('specialisations', []):
            # Tag may already exist; we'll link it to the first sector if provided
            tag_sector = sectors[0] if sectors else None
            tag = get_or_create_tag(tag_name.strip(), tag_sector)
            donor.specialisations.add(tag)

        donor.save()
        return donor

    # ------------------------------------------------------------------
    # 1. HEALTH SECTOR DONORS
    # ------------------------------------------------------------------
    health_sector = get_or_create_sector('Health')

    health_donors = [
        {
            'name': 'Mastercard Foundation',
            'donation_type': 'Economic Empowerment',
            'fundraising_frequency': 'Institution to institution engagement',
            'what_is_required': 'CEO to pitch',
            'website': 'https://mastercardfdn.org/',
            'sectors': ['Health'],
            'specialisations': ['Youth empowerment', 'SRH', 'Practical skills'],
            'donor_relationship_strategy': 'Success stories and gaps',
            'contact_person': 'Contacts',
            'notes': '',
        },
        {
            'name': 'Wellcome Trust',
            'donation_type': 'Research for health',
            'fundraising_frequency': 'Many calls with varied deadlines',
            'what_is_required': 'Proposal to WT and Bid to SFA',
            'website': 'https://wellcome.org/',
            'sectors': ['Health'],
            'specialisations': ['Climate and Health', 'Mental Health', 'Clinical Trials', 'Capacity Building', 'Malaria', 'HIV', 'TB'],
            'donor_relationship_strategy': 'Link-up with SFA for collaboration',
            'contact_person': 'Contacts',
            'notes': 'Supports partnerships between Africa and Europe',
        },
        {
            'name': 'EDCTP Association',
            'donation_type': 'Research Grants',
            'fundraising_frequency': 'Periodic calls',
            'what_is_required': 'Proposal',
            'website': 'https://www.edctp.org/about-us/',
            'sectors': ['Health'],
            'specialisations': ['Clinical Trials', 'Capacity Building'],
            'donor_relationship_strategy': 'Build consortia and submit to calls',
            'contact_person': 'Head Office- The Hague, Regional Office- Cape Town',
            'notes': 'Supported by the European Union',
        },
        {
            'name': 'WHO',
            'donation_type': 'Technical Support',
            'fundraising_frequency': 'Direct partnerships',
            'what_is_required': 'Proposal and Bid',
            'website': 'https://www.afro.who.int/countries/kenya',
            'sectors': ['Health'],
            'specialisations': ['Global Health Policy', 'Disease Control'],
            'donor_relationship_strategy': 'Success stories and gaps',
            'contact_person': 'Kenya Office Contact',
            'contact_email': 'afkenwr@who.int',
            'contact_phone': '+254 20 2717902',
            'notes': 'Focus on strengthening health systems',
        },
        {
            'name': 'National Institute of Health (NIH)',
            'donation_type': 'Research Funding',
            'fundraising_frequency': 'Develop collaborative networks',
            'what_is_required': 'Annual calls',
            'website': 'https://grants.nih.gov/',
            'sectors': ['Health'],
            'specialisations': ['Biomedical', 'Public Health Research'],
            'donor_relationship_strategy': 'Success stories and gaps',
            'notes': 'Strong focus on capacity building and innovation',
        },
        {
            'name': 'Medical Research Council (UK)',
            'donation_type': 'Research Grants',
            'fundraising_frequency': 'Submit applications to open calls',
            'what_is_required': 'Biannual calls',
            'website': 'https://www.ukri.org/councils/mrc/',
            'sectors': ['Health'],
            'specialisations': ['Biomedical', 'Health Research'],
            'donor_relationship_strategy': 'Establish partnerships with UK institutions',
            'notes': 'Often co-funds with other agencies',
        },
        {
            'name': 'British Council',
            'donation_type': 'Grants',
            'fundraising_frequency': 'Proposals',
            'what_is_required': 'Open Concept notes',
            'website': 'https://www.britishcouncil.org/',
            'sectors': ['Health', 'Education'],
            'specialisations': ['Education', 'Research'],
            'donor_relationship_strategy': 'Strengthen institutional collaborations',
        },
        {
            'name': 'Bill & Melinda Gates Foundation',
            'donation_type': 'Grants',
            'fundraising_frequency': 'Rolling applications',
            'what_is_required': 'Proposal or concept note',
            'website': 'https://www.gatesfoundation.org/',
            'sectors': ['Health', 'Agriculture'],
            'specialisations': ['Infectious Diseases', 'Maternal & Child Health'],
            'donor_relationship_strategy': 'Leverage strong success stories in impact',
            'notes': 'Focuses on scalable and impactful solutions',
        },
        {
            'name': 'Malaria Consortium',
            'donation_type': 'Research Funding',
            'fundraising_frequency': 'Program-specific',
            'what_is_required': 'Proposals',
            'website': 'https://www.malariaconsortium.org/',
            'sectors': ['Health'],
            'specialisations': ['Malaria Control', 'Malaria Elimination'],
            'donor_relationship_strategy': 'Build partnerships with their regional programs',
            'contact_email': 'info@malariaconsortium.org',
            'notes': 'Expertise in malaria-focused health programs',
        },
        {
            'name': 'International Development Research Centre (IDRC)',
            'donation_type': 'Grants',
            'fundraising_frequency': 'Annual calls',
            'what_is_required': 'Proposal/Concept notes',
            'website': 'https://idrc-crdi.ca/en',
            'sectors': ['Health'],
            'specialisations': ['Research and Development'],
            'donor_relationship_strategy': 'Highlight impact of past collaborations',
        },
        {
            'name': 'Pfizer Foundation',
            'donation_type': 'Grants',
            'fundraising_frequency': 'Program-specific',
            'what_is_required': 'Proposal',
            'website': 'https://www.pfizer.com/',
            'sectors': ['Health'],
            'specialisations': ['Global Health Initiatives'],
            'donor_relationship_strategy': 'Engage in CSR-focused partnerships',
        },
        {
            'name': 'German Research Foundation (DFG)',
            'donation_type': 'Research Grants',
            'fundraising_frequency': 'Periodic calls',
            'what_is_required': 'Proposal',
            'website': 'https://www.dfg.de/',
            'sectors': ['Health'],
            'specialisations': ['Science and Humanities'],
            'donor_relationship_strategy': 'Build collaborative research proposals',
        },
        {
            'name': 'Global Health Corps',
            'donation_type': 'Fellowships',
            'fundraising_frequency': 'Annual recruitment',
            'what_is_required': 'Application or proposal',
            'website': 'https://ghcorps.org/',
            'sectors': ['Health'],
            'specialisations': ['Leadership in Global Health'],
            'donor_relationship_strategy': 'Success stories and gaps',
        },
        {
            'name': 'Africa Centres for Disease Control and Prevention (Africa CDC)',
            'donation_type': 'Grants/Technical Aid',
            'fundraising_frequency': 'Program-specific',
            'what_is_required': 'Proposal',
            'website': 'https://africacdc.org/',
            'sectors': ['Health'],
            'specialisations': ['Public Health Surveillance', 'Research Capacity'],
            'donor_relationship_strategy': 'Leverage partnerships with regional institutions',
            'notes': 'Focus on public health emergencies',
        },
        {
            'name': 'Fogarty International Center (NIH)',
            'donation_type': 'Fellowships/Grants',
            'fundraising_frequency': 'Annual calls',
            'what_is_required': 'Proposal',
            'website': 'https://www.fic.nih.gov/',
            'sectors': ['Health'],
            'specialisations': ['Global Health Training', 'Global Health Research'],
            'donor_relationship_strategy': 'Build consortia and partnerships with U.S. institutions',
            'notes': 'Focuses on research and training in Africa',
        },
        {
            'name': 'DAAD',
            'donation_type': 'Fellowships/Grants',
            'fundraising_frequency': 'Annual calls',
            'what_is_required': 'Proposals',
            'website': 'https://www.daad.de/en/studying-in-germany/scholarships/daad-scholarships/',
            'sectors': ['Health'],
            'specialisations': ['Research projects', 'Capacity building'],
            'donor_relationship_strategy': 'Leverage on partnerships',
        },
        # Local Health Partners
        {
            'name': 'African Population & Health Research Center (APHRC)',
            'donation_type': 'Grants',
            'fundraising_frequency': 'Rolling calls',
            'what_is_required': 'Proposals/concept Note',
            'website': 'https://aphrc.org/',
            'sectors': ['Health'],
            'specialisations': ['Health and development', 'Policy development', 'Capacity building'],
            'donor_relationship_strategy': 'Leverage on partnerships',
        },
        {
            'name': 'Safaricom Foundation',
            'donation_type': 'CSR Donations',
            'fundraising_frequency': 'Ongoing',
            'what_is_required': 'Proposal or pitch',
            'website': 'https://www.safaricomfoundation.org/',
            'sectors': ['Health', 'Education'],
            'specialisations': ['Education', 'Health', 'Economic Empowerment'],
            'donor_relationship_strategy': 'Showcase success stories in Kenya',
        },
        {
            'name': 'Coca-Cola Company',
            'donation_type': 'CSR Donations',
            'fundraising_frequency': 'Ongoing',
            'what_is_required': 'Proposal',
            'website': 'https://www.coca-colacompany.com/',
            'sectors': ['Health'],
            'specialisations': ['Water', 'Health', 'Community Empowerment'],
            'donor_relationship_strategy': 'Leverage their CSR focus on community projects',
        },
        {
            'name': 'SFA (Science for Africa)',
            'donation_type': 'Research Funding',
            'fundraising_frequency': 'Multiple calls annually',
            'what_is_required': 'Proposal or bid',
            'website': 'https://scienceforafrica.foundation/',
            'sectors': ['Health'],
            'specialisations': ['Science', 'Technology', 'Innovation'],
            'donor_relationship_strategy': 'Link up with existing research institutions',
        },
        {
            'name': 'Liquid Telecom',
            'donation_type': 'Infrastructure',
            'fundraising_frequency': 'Program-specific',
            'what_is_required': 'Proposals/Pitch',
            'website': 'https://liquid.tech/',
            'sectors': ['Health'],
            'specialisations': ['ICT Infrastructure Development'],
            'donor_relationship_strategy': 'Showcase ICT-enabled health and research projects',
        },
    ]

    for donor_data in health_donors:
        create_donor(donor_data)

    # ------------------------------------------------------------------
    # 2. AGRICULTURE SECTOR DONORS
    # ------------------------------------------------------------------
    agriculture_sector = get_or_create_sector('Agriculture')

    agriculture_donors = [
        {
            'name': 'Alliance for the Green Revolution in Africa (AGRA)',
            'donation_type': 'Grants, technical assistance, and capacity building for smallholder farmers',
            'fundraising_frequency': 'Annual call for proposals',
            'what_is_required': 'Proposal submission through a specific portal',
            'website': 'https://agra.org/',
            'sectors': ['Agriculture'],
            'specialisations': ['Sustainable agriculture', 'Smallholder farmers support'],
            'donor_relationship_strategy': 'Describe past engagements, challenges, and future relationship strategies',
        },
        {
            'name': 'FAO (Food and Agriculture Organization)',
            'donation_type': 'Technical expertise, policy support, and capacity development in agriculture and food security',
            'fundraising_frequency': 'Rolling funding calls',
            'what_is_required': 'Formal proposal and partnership agreements',
            'website': 'https://www.fao.org/',
            'sectors': ['Agriculture'],
            'specialisations': ['Food security', 'Climate resilience', 'Sustainable agriculture'],
            'donor_relationship_strategy': 'Describe previous collaborations and future engagement strategies',
        },
        {
            'name': 'One Acre Fund',
            'donation_type': 'Financing, training, and distribution of agricultural inputs to smallholder farmers',
            'fundraising_frequency': 'Periodic funding rounds',
            'what_is_required': 'Business pitch and proposal',
            'website': 'https://oneacrefund.org/',
            'sectors': ['Agriculture'],
            'specialisations': ['Smallholder farmer financing', 'Agri-input distribution'],
            'donor_relationship_strategy': 'Mention how relationships have been developed and sustained',
        },
        {
            'name': 'European Union',
            'donation_type': 'Grants and funding programs for agricultural development, research, and innovation',
            'fundraising_frequency': 'Multi-year funding cycles',
            'what_is_required': 'Competitive bid and project proposal',
            'website': 'https://ec.europa.eu/',
            'sectors': ['Agriculture'],
            'specialisations': ['Research', 'Innovation', 'Policy advocacy'],
            'donor_relationship_strategy': 'Mention past engagements, challenges, and future relationship strategies',
        },
        {
            'name': 'Agri Kenya Challenge Fund',
            'donation_type': 'Competitive grants to agri-businesses for innovative projects in agriculture',
            'fundraising_frequency': 'Annual challenge fund',
            'what_is_required': 'Business case pitch and application',
            'website': 'https://www.agrichallengefund.org/',
            'sectors': ['Agriculture'],
            'specialisations': ['Agri-business innovation', 'Rural development'],
            'donor_relationship_strategy': 'Discuss engagement success and improvement areas',
        },
        {
            'name': 'Wangari Maathai Belt Movement',
            'donation_type': 'Support for environmental conservation and tree planting initiatives',
            'fundraising_frequency': 'Periodic or project-based funding',
            'what_is_required': 'Concept note and partnership proposal',
            'website': 'https://www.greenbeltmovement.org/',
            'sectors': ['Agriculture', 'Environment'],
            'specialisations': ['Environmental conservation', 'Women\'s leadership'],
            'donor_relationship_strategy': 'Describe collaboration effectiveness and donor expectations',
        },
        {
            'name': 'Ford Foundation',
            'donation_type': 'Grants for social justice initiatives, including economic development and human rights',
            'fundraising_frequency': 'Multi-year grants',
            'what_is_required': 'Full proposal submission',
            'website': 'https://www.fordfoundation.org/',
            'sectors': ['Agriculture'],
            'specialisations': ['Social justice', 'Economic inclusion'],
            'donor_relationship_strategy': 'Describe past engagements, success, and challenges',
        },
        {
            'name': 'Africa Harvest',
            'donation_type': 'Grants, technical assistance',
            'fundraising_frequency': 'Rolling basis',
            'what_is_required': 'Detailed proposals outlining project objectives and outcomes',
            'website': 'https://africaharvest.org/',
            'sectors': ['Agriculture'],
            'specialisations': ['Agriculture', 'Food security'],
            'donor_relationship_strategy': 'Describe past collaborations, successes, and areas for improvement',
            'contact_email': 'info@africaharvest.org',
            'contact_person': 'P.O Box 642 – 00621 Spring Valley, Nairobi, Kenya',
        },
        {
            'name': 'GIZ (Deutsche Gesellschaft für Internationale Zusammenarbeit)',
            'donation_type': 'Technical cooperation, capacity development, and policy advice',
            'fundraising_frequency': 'Rolling basis',
            'what_is_required': 'Detailed proposals outlining project objectives and outcomes',
            'website': 'https://www.giz.de/',
            'sectors': ['Agriculture'],
            'specialisations': ['Sustainable development', 'Agriculture', 'Economic development'],
            'donor_relationship_strategy': 'Describe past collaborations, successes, and areas for improvement',
        },
        {
            'name': 'International Fund for Agricultural Development (IFAD)',
            'donation_type': 'Grants and low-interest loans for agricultural development projects',
            'fundraising_frequency': 'Regular calls for proposals',
            'what_is_required': 'Comprehensive project proposals with clear impact metrics',
            'website': 'https://www.ifad.org/',
            'sectors': ['Agriculture'],
            'specialisations': ['Rural poverty alleviation', 'Smallholder agriculture', 'Food security'],
            'donor_relationship_strategy': 'Highlight successful projects and identify potential gaps in engagement',
        },
        {
            'name': 'World Bank',
            'donation_type': 'Financial and technical assistance for development projects',
            'fundraising_frequency': 'Annual and rolling funding opportunities',
            'what_is_required': 'Formal proposals aligned with funding priorities',
            'website': 'https://www.worldbank.org/',
            'sectors': ['Agriculture', 'Infrastructure'],
            'specialisations': ['Global development', 'Poverty reduction', 'Infrastructure', 'Agriculture'],
            'donor_relationship_strategy': 'Discuss previous partnerships, successes, and areas needing attention',
        },
        {
            'name': 'International Finance Corporation (IFC)',
            'donation_type': 'Investments and advisory services to promote private sector development',
            'fundraising_frequency': 'Ongoing investment opportunities',
            'what_is_required': 'Investment proposals and business plans',
            'website': 'https://www.ifc.org/',
            'sectors': ['Agriculture'],
            'specialisations': ['Private sector development', 'Financial inclusion', 'Infrastructure'],
            'donor_relationship_strategy': 'Outline successful collaborations and areas for relationship enhancement',
        },
        {
            'name': 'United States Agency for International Development (USAID)',
            'donation_type': 'Grants, technical assistance, and humanitarian aid',
            'fundraising_frequency': 'Regular funding opportunities',
            'what_is_required': 'Proposals responding to specific funding announcements',
            'website': 'https://www.usaid.gov/',
            'sectors': ['Agriculture', 'Health'],
            'specialisations': ['Global development', 'Health', 'Education', 'Agriculture', 'Democracy promotion'],
            'donor_relationship_strategy': 'Detail past successes and identify gaps in donor engagement',
        },
        {
            'name': 'International Livestock Research Institute (ILRI)',
            'donation_type': 'Research funding, technical support, and capacity building',
            'fundraising_frequency': 'Periodic funding calls',
            'what_is_required': 'Research proposals with clear objectives and methodologies',
            'website': 'https://www.ilri.org/',
            'sectors': ['Agriculture'],
            'specialisations': ['Livestock research', 'Sustainable agriculture', 'Food security'],
            'donor_relationship_strategy': 'Highlight collaborative research successes and areas for improvement',
        },
        {
            'name': 'African Development Bank (AfDB)',
            'donation_type': 'Loans, grants, and technical assistance for development projects',
            'fundraising_frequency': 'Regular funding cycles',
            'what_is_required': 'Formal project proposals with feasibility studies',
            'website': 'https://www.afdb.org/',
            'sectors': ['Agriculture', 'Infrastructure'],
            'specialisations': ['Economic development', 'Poverty reduction', 'Infrastructure', 'Agriculture'],
            'donor_relationship_strategy': 'Outline past partnership successes and areas needing attention',
        },
        {
            'name': 'BROOKE International',
            'donation_type': 'Grants and support for animal welfare programs',
            'fundraising_frequency': 'Annual funding opportunities',
            'what_is_required': 'Project proposals with clear animal welfare objectives',
            'website': 'https://www.thebrooke.org/',
            'sectors': ['Agriculture'],
            'specialisations': ['Equine welfare', 'Animal health', 'Community development'],
            'donor_relationship_strategy': 'Highlight successful programs and identify engagement gaps',
        },
    ]

    for donor_data in agriculture_donors:
        create_donor(donor_data)

    # ------------------------------------------------------------------
    # Additional donors from the Action Plan list (local)
    # These are briefly mentioned; we add them with basic info.
    # ------------------------------------------------------------------
    additional_donors = [
        {
            'name': 'GAIN',
            'donation_type': 'Grants',
            'fundraising_frequency': 'Program-specific',
            'what_is_required': 'Proposal',
            'sectors': ['Health', 'Agriculture'],
            'specialisations': ['Nutrition', 'Food systems'],
            'notes': 'Global Alliance for Improved Nutrition',
        },
        {
            'name': 'STAK (Self-help groups - DFID)',
            'donation_type': 'Grants',
            'fundraising_frequency': 'Periodic',
            'what_is_required': 'Proposal',
            'sectors': ['Agriculture'],
            'specialisations': ['Self-help groups', 'Livelihoods'],
            'notes': 'DFID-funded program',
        },
        {
            'name': 'CGIAR',
            'donation_type': 'Research Funding',
            'fundraising_frequency': 'Rolling',
            'what_is_required': 'Proposal',
            'sectors': ['Agriculture'],
            'specialisations': ['Agricultural research', 'Food security'],
            'website': 'https://www.cgiar.org/',
        },
        {
            'name': 'World Agroforestry (ICRAF)',
            'donation_type': 'Research Funding',
            'fundraising_frequency': 'Periodic',
            'what_is_required': 'Proposal',
            'sectors': ['Agriculture', 'Environment'],
            'specialisations': ['Agroforestry', 'Sustainable land use'],
            'website': 'https://www.worldagroforestry.org/',
        },
        {
            'name': 'Water Mission',
            'donation_type': 'Technical Support',
            'fundraising_frequency': 'Program-specific',
            'what_is_required': 'Proposal',
            'sectors': ['Agriculture', 'WASH'],
            'specialisations': ['Water access', 'Sanitation', 'Hygiene'],
            'website': 'https://watermission.org/',
        },
        {
            'name': 'CETRAD - Nanyuki',
            'donation_type': 'Research Support',
            'fundraising_frequency': 'Periodic',
            'what_is_required': 'Proposal',
            'sectors': ['Agriculture'],
            'specialisations': ['Dryland agriculture', 'Natural resource management'],
            'notes': 'Center for Training and Research in Arid and Semi-Arid Lands',
        },
        {
            'name': 'Farm Africa',
            'donation_type': 'Grants and technical support',
            'fundraising_frequency': 'Program-specific',
            'what_is_required': 'Proposal',
            'sectors': ['Agriculture'],
            'specialisations': ['Sustainable agriculture', 'Market access'],
            'website': 'https://www.farmafrica.org/',
        },
        {
            'name': 'Green Climate Fund - UNEP',
            'donation_type': 'Grants/Climate Finance',
            'fundraising_frequency': 'Periodic',
            'what_is_required': 'Proposal',
            'sectors': ['Environment', 'Agriculture'],
            'specialisations': ['Climate change adaptation', 'Mitigation'],
            'website': 'https://www.greenclimate.fund/',
        },
        {
            'name': 'Adaptation Fund',
            'donation_type': 'Grants/Climate Finance',
            'fundraising_frequency': 'Periodic',
            'what_is_required': 'Proposal',
            'sectors': ['Environment', 'Agriculture'],
            'specialisations': ['Climate adaptation', 'Resilience'],
            'website': 'https://www.adaptation-fund.org/',
        },
        {
            'name': 'Climate Justice Resilience Fund',
            'donation_type': 'Grants',
            'fundraising_frequency': 'Periodic',
            'what_is_required': 'Proposal',
            'sectors': ['Environment'],
            'specialisations': ['Climate justice', 'Community resilience'],
        },
        {
            'name': 'LEWA - Confirm',
            'donation_type': 'Grants',
            'fundraising_frequency': 'Program-specific',
            'what_is_required': 'Proposal',
            'sectors': ['Environment', 'Wildlife'],
            'specialisations': ['Wildlife conservation', 'Community development'],
            'notes': 'Lewa Wildlife Conservancy',
        },
        {
            'name': 'Dutch Fund for Climate and Development',
            'donation_type': 'Climate Finance',
            'fundraising_frequency': 'Periodic',
            'what_is_required': 'Proposal',
            'sectors': ['Environment', 'Agriculture'],
            'specialisations': ['Climate adaptation', 'Sustainable development'],
            'website': 'https://www.dutchfundclimate.com/',
        },
        {
            'name': 'Agricultural Finance Corporation (AFC) - Local',
            'donation_type': 'Loans/Financing',
            'fundraising_frequency': 'Ongoing',
            'what_is_required': 'Loan application',
            'sectors': ['Agriculture'],
            'specialisations': ['Agricultural finance', 'Agribusiness'],
            'notes': 'Kenya-based agricultural financing institution',
        },
    ]

    for donor_data in additional_donors:
        create_donor(donor_data)

    print("Donor population complete.")


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0002_auto_add_lookup_data'),  # adjust to your latest migration
    ]

    operations = [
        migrations.RunPython(create_choices),
    ]