from graphql.ast import (
    Field,
    FragmentSpread,
    InlineFragment,
)


def get_selections(selections, fragments, object_type, seen_fragments=None):
    _selections = []

    if seen_fragments is None:
        seen_fragments = set()

    for selection in selections:
        if isinstance(selection, Field):
            _selections.append(selection)
            continue

        if isinstance(selection, FragmentSpread):
            fragment = fragments[selection.name]
        elif isinstance(selection, InlineFragment):
            fragment = selection

        # If the fragment doesn't apply to the current object, don't
        # add its selections. This could happen for example if this is
        # a union of different object types with different fields for
        # each type.
        if fragment.type_condition.name != object_type.object_name:
            continue

        # Skip fragments we've already seen to avoid recursion issues.
        if hasattr(fragment, 'name'):
            if fragment.name in seen_fragments:
                continue
            else:
                seen_fragments.add(fragment.name)

        _selections += get_selections(
            selections=fragment.selections,
            fragments=fragments,
            object_type=object_type,
            seen_fragments=seen_fragments,
        )

    return _selections
