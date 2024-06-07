def get_posts(post):
    return post.custom_manager.select_related('author',
                                              'category',
                                              'location',)
