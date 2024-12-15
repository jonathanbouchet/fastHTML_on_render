from fasthtml.common import *

def render(contact):
    return Li(f"{contact.name} - {contact.email}",
              A(
                  " Delete", 
                  hx_delete=f"/delete/{contact.id}", 
                  hx_swap="outerHTML",
                  target_id=f"contact-{contact.id}"), 
                id=f"contact-{contact.id}")

app, rt, contacts, Contact = fast_app(
    "contacts.db", 
    live=True,
    render=render,
    id=int,
    name=str,
    email=str,
    pk="id")

# create fake contacts
fake_contacts = [
    {"name":"john doe", "email":"johndoe@example.com"},
    {"name":"jane doe", "email":"janedoe@example.com"},
    {"name":"Kevin Bacon", "email":"kevin@example.com"}
]

def create_contacts():
    if len(contacts()) == 0:
        for c in fake_contacts:
            contacts.insert(Contact(name=c['name'], email=c['email']))

def reset_name_input():
    """used to clear name input after submission

    :return _type_: _description_
    """
    return Input(id="name", placeholder="Username", hx_swap_oob="true")

def reset_email_input():
    """used to clear email input after submission

    :return _type_: _description_
    """
    return Input(id="email", placeholder="Email", hx_swap_oob="true")

@rt("/")
def get():
    create_contacts()
    return Titled(
        "Contact Book",
        Div(
            Ul(*contacts(), id="contacts_list"),
            Form(
                reset_name_input(),
                reset_email_input(),
            Button(
                "Add contact", 
                style="border-radius: 8px", 
                hx_post="/add",
                target_id="contacts_list",
                hx_swap="beforeend"
                # onclick="alert('Hello World')"
                )
            )
        )
    )

@rt("/add")
def add(contact: Contact):
    contacts.insert(contact)
    return contact, reset_name_input(), reset_email_input()

@rt("/delete/{id}")
def delete(id: int):
    contacts.delete(id)
