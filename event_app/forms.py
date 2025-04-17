from django import forms
from event_app.models import Event,Participant,Category

class FormModelStyleMixin:
    base_style='border-2 p-2  border-gray-500 rounded-lg bg-white hover:bg-gray-50 text-green-800 '
    base_style_unCommon='focus:outline-none focus:border-green-500'
    def style_all_field(self):
        
        for field_name,field in self.fields.items():
            if isinstance(field.widget,forms.TimeInput):
                field.widget.attrs.update({
                    'class':f'{self.base_style + self.base_style_unCommon} w-3/5 m-2',
                })
            elif isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':f'{self.base_style + self.base_style_unCommon} w-full',
                    'placeholder':f'Enter {field.label.lower()}',
                    
                })

            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':f'{self.base_style + self.base_style_unCommon} w-full',
                    'placeholder':f'Enter {field.label.lower()}',
                    'rows':4,
                    
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class':f'{self.base_style + self.base_style_unCommon} w-auto',  
                })
            elif isinstance(field.widget,forms.Select):
                field.widget.attrs.update({
                    'class':f'{self.base_style + self.base_style_unCommon} w-full',
                    'placeholder':f'Enter your{field.label.lower()}'  
                })
            elif isinstance(field.widget,forms.EmailInput):
                field.widget.attrs.update({
                    'class':f'{self.base_style + self.base_style_unCommon} w-full',
                    'placeholder':f'Enter your {field.label.lower() } address ',
                    
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':f'{self.base_style}',  
                })
            
                

                
            

class EventForm(FormModelStyleMixin,forms.ModelForm):
    class Meta:
        model=Event
        fields=['name','description','location','date','time']
        labels={
            'name':'Event Name',
            'description':'Event Description',
            'location':'Event Location Like (city-country)',
            'date':'Event Date',
            'time':'Event Time',
        }
        widgets={
            'name':forms.TextInput,
            'description':forms.Textarea,
            'date':forms.SelectDateWidget,
            'time':forms.TimeInput(attrs={
                                        'type':'time'
                                         }),
            
             
        }



    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.style_all_field()




class EventCategoryModelForm(FormModelStyleMixin,forms.ModelForm):
    

    class Meta:
        model=Category
        fields=['category_name','category_description']
        widgets={
            'category_name':forms.Select,
            'category_description':forms.Textarea,
        }
        labels={
            'category_name':'Select Category',
            'category_description':'Category Description',
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.style_all_field()



class ParticipantModelForm(FormModelStyleMixin,forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.style_all_field()

    class Meta:
        model=Participant
        fields='__all__'
        labels={
            'events':'Select Events'
        }
        widgets={
            'name':forms.TextInput,
            'email':forms.EmailInput,
            'events':forms.CheckboxSelectMultiple,
        }
