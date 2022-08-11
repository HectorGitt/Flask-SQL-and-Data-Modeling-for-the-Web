from datetime import datetime
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
    def model_control(self,model,type):
        
        past_shows = []
        upcoming_shows = []
        past_shows_count = 0
        upcoming_shows_count = 0
        genres = []
        for genre in model.genres:
            genres.append(genre)
        #define time based on page request time
        time = datetime.now()
        for show in model.shows:
            if show.start_time < time:
                past_shows.append({
                    "venue_id": show.venue_id,
                    "venue_name": show.venue.name,
                    "venue_image_link": show.venue.image_link,
                    "start_time": str(show.start_time)
                })
                past_shows_count += 1
            else:
                upcoming_shows.append({
                    "venue_id": show.venue_id,
                    "venue_name": show.venue.name,
                    "venue_image_link": show.venue.image_link,
                    "start_time": str(show.start_time)
                })
                upcoming_shows_count += 1
        data = {
            "id": model.id,
            "name": model.name,
            "city": model.city,
            "state": model.state,
            "phone": model.phone,
            "genres" : genres,
            "website": model.website_link,
            "facebook_link": model.facebook_link,
            "seeking_description": model.seeking_description,
            "image_link": model.image_link,
            "past_shows": past_shows,
            "past_shows_count": past_shows_count,
            "upcoming_shows": upcoming_shows,
            "upcoming_shows_count": upcoming_shows_count
        }
        
        
        if type=='artist':
            
            data["seeking_venue"] = model.seeking_venue
        else:
            data["address"] = model.address
            data["seeking_talent"] = model.seeking_talent
        return data
    def edit_get(self,form,model,type):
        form.name.data = model.name
        form.city.data = model.city
        form.state.data = model.state
        form.phone.data = model.phone
        form.facebook_link.data = model.facebook_link
        form.image_link.data = model.image_link
        form.website_link.data = model.website_link
        form.seeking_description.data = model.seeking_description
        if type=='artist':
            form.seeking_venue.data = model.seeking_venue
        else:
            form.address.data = model.address
            form.seeking_talent.data = model.seeking_talent
        
    def edit_post(self,form,model,type):
        name = form.name.data
        city = form.city.data
        state = form.state.data
        phone = form.phone.data
        image_link = form.image_link.data
        facebook_link = form.facebook_link.data
        website_link = form.website_link.data
        seeking_description = form.seeking_description.data
        
        #change model fields to new edit
        model.name=name
        model.city=city
        model.state=state
        model.phone=phone
        model.image_link=image_link
        model.facebook_link=facebook_link
        model.website_link=website_link
        model.seeking_description=seeking_description
        if type=='artist':
            seeking_venue= form.seeking_venue.data
            model.seeking_venue=seeking_venue
        else:
            address = form.address.data
            seeking_talent= form.seeking_talent.data
            model.address=address
            model.seeking_talent=seeking_talent
        