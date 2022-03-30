

jwtToken = request.cookies.get('jwt-token')
    if jwtToken is None : return render_template('index.html', loginChecked = "true", homeDict = homeDict)

    try: 
        jti = decode_token(jwtToken)['jti']
        user = decode_token(jwtToken).get(config.identity_claim_key, None)
    except ExpiredSignatureError:
        return render_template('index.html', loginChecked = "true", homeDict = homeDict)
    
    loginChecked = jti in jwt_blocklist
    return render_template('index.html', homeDict = homeDict, loginChecked = loginChecked, username = user)