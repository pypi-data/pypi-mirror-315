operation_parameter_map = {
    '/validate-email-POST': {
        'parameters': [
        ]
    },
    '/messages-GET': {
        'parameters': [
            {
                'name': 'Accept'
            },
        ]
    },
    '/messages-POST': {
        'parameters': [
            {
                'name': 'Content-Type'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/messages/{uid}/delete-POST': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/messages/{uid}-GET': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/messages/{uid}-PATCH': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Content-Type'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/messages/{uid}/pause-POST': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/messages/{uid}/resume-POST': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/lists-GET': {
        'parameters': [
            {
                'name': 'Accept'
            },
        ]
    },
    '/lists-POST': {
        'parameters': [
            {
                'name': 'Content-Type'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/lists/{uid}/add-field-POST': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Content-Type'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/lists/{uid}/delete-POST': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/lists/{uid}-GET': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/lists/{uid}-PATCH': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Content-Type'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/relay/emails/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'limit'
            },
        ]
    },
    '/relay/raw-POST': {
        'parameters': [
            {
                'name': 'message'
            },
            {
                'name': 'is_transactional'
            },
            {
                'name': 'track_click'
            },
            {
                'name': 'track_open'
            },
            {
                'name': 'sign_dkim'
            },
        ]
    },
    '/relay/send-POST': {
        'parameters': [
        ]
    },
    '/contacts-GET': {
        'parameters': [
            {
                'name': 'Accept'
            },
            {
                'name': 'email'
            },
            {
                'name': 'per_page'
            },
            {
                'name': 'page'
            },
        ]
    },
    '/contacts-POST': {
        'parameters': [
            {
                'name': 'Content-Type'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/contacts/{uid}/add-tag-POST': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Content-Type'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/contacts/{uid}/delete-POST': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/contacts/{uid}-GET': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/contacts/{uid}-PATCH': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Content-Type'
            },
            {
                'name': 'Accept'
            },
        ]
    },
    '/contacts/{uid}/subscribe-PATCH': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Accept'
            },
            {
                'name': 'list_uid'
            },
        ]
    },
    '/contacts/{uid}/unsubscribe-PATCH': {
        'parameters': [
            {
                'name': 'uid'
            },
            {
                'name': 'Accept'
            },
            {
                'name': 'list_uid'
            },
        ]
    },
};