TYPE_MAPPING = {
    'unicode': 'string',
    'string': 'string',
    'integer': 'integer'
}

def get_synonymous(term):
    return TYPE_MAPPING[term] if term in TYPE_MAPPING else term