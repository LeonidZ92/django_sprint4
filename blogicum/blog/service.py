def get_posts(post):
    return post.published_manager.select_related('author',
                                                 'category',
                                                 'location',)
