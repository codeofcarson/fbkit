from .. import proxies

BINDINGS = {
    'publishStoryToUser': [
        ('title', str, {}),
        ('body', str, {'optional': True}),
        ('image_1', str, {'optional': True}),
        ('image_1_link', str, {'optional': True}),
        ('image_2', str, {'optional': True}),
        ('image_2_link', str, {'optional': True}),
        ('image_3', str, {'optional': True}),
        ('image_3_link', str, {'optional': True}),
        ('image_4', str, {'optional': True}),
        ('image_4_link', str, {'optional': True}),
        ('priority', int, {'optional': True}),
    ],
    'publishActionOfUser': [
        ('title', str, {}),
        ('body', str, {'optional': True}),
        ('image_1', str, {'optional': True}),
        ('image_1_link', str, {'optional': True}),
        ('image_2', str, {'optional': True}),
        ('image_2_link', str, {'optional': True}),
        ('image_3', str, {'optional': True}),
        ('image_3_link', str, {'optional': True}),
        ('image_4', str, {'optional': True}),
        ('image_4_link', str, {'optional': True}),
        ('priority', int, {'optional': True}),
    ],
    'publishTemplatizedAction': [
        ('title_template', str, {}),
        ('page_actor_id', int, {'optional': True}),
        ('title_data', proxies.json, {'optional': True}),
        ('body_template', str, {'optional': True}),
        ('body_data', proxies.json, {'optional': True}),
        ('body_general', str, {'optional': True}),
        ('image_1', str, {'optional': True}),
        ('image_1_link', str, {'optional': True}),
        ('image_2', str, {'optional': True}),
        ('image_2_link', str, {'optional': True}),
        ('image_3', str, {'optional': True}),
        ('image_3_link', str, {'optional': True}),
        ('image_4', str, {'optional': True}),
        ('image_4_link', str, {'optional': True}),
        ('target_ids', list, {'optional': True}),
    ],
    'registerTemplateBundle': [
        ('one_line_story_templates', proxies.json, {}),
        ('short_story_templates', proxies.json, {'optional': True}),
        ('full_story_template', proxies.json, {'optional': True}),
        ('action_links', proxies.json, {'optional': True}),
    ],
    'deactivateTemplateBundleByID': [
        ('template_bundle_id', int, {}),
    ],
    'getRegisteredTemplateBundles': {},
    'getRegisteredTemplateBundleByID': [
        ('template_bundle_id', str, {}),
    ],
    'publishUserAction': [
        ('template_bundle_id', int, {}),
        ('template_data', proxies.json, {'optional': True}),
        ('target_ids', list, {'optional': True}),
        ('body_general', str, {'optional': True}),
        ('story_size', int, {'optional': True}),
    ],
}

Proxy = proxies.build_proxy('feed', BINDINGS)
