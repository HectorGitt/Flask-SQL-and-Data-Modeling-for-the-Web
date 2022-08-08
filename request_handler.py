class Request:
    
    def __init__(self):
        pass
    
    def request_control(self,form,model,type):
        name = form.name.data
        city = form.city.data
        state = form.state.data
        phone = form.phone.data
        image_link = form.image_link.data
        genres = form.genres.data
        facebook_link = form.facebook_link.data
        website_link = form.website_link.data
        seeking_description = form.seeking_description.data
        if type=='venue':
            address = form.address.data
            seeking_talent = form.seeking_talent.data
            venue = model(
                name=name,
                city=city,
                state=state,
                address=address,
                phone=phone,
                image_link=image_link,
                facebook_link=facebook_link,
                website_link=website_link,
                seeking_talent=seeking_talent,
                seeking_description=seeking_description,
            )
            return venue, genres
        else:
            seeking_venue = form.seeking_venue.data
            artist = model(
                name=name,
                city=city,
                state=state,
                phone=phone,
                image_link=image_link,
                facebook_link=facebook_link,
                website_link=website_link,
                seeking_venue=seeking_venue,
                seeking_description=seeking_description,
            )
            return artist, genres
        