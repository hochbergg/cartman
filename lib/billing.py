import braintree

def fine_user(username, amount):
    customer = braintree.Customer.find(username)
    mthd_token = customer.payment_methods[0].token
    braintree.Transaction.sale({
        "amount": str(amount),
        "payment_method_token": mthd_token
    })