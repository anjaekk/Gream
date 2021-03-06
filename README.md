# ๐ผ Gream

## ๐ ํ๋ก์ ํธ ๊ฐ์
- **Kream ์ฌ์ดํธ๋ฅผ ๋ชจํฐ๋ธ๋ก ๊ทธ๋ฆผ ํ๋งค ์ฌ์ดํธ ๊ตฌํ ํ๋ก์ ํธ**
- **๊ธฐ ๊ฐ**: 2021.07.19.~2021.07.30.(12์ผ)
- **Team member**
  - Frontend: 3์ธ(๋ฐ์ ํ, ์ค์ง์, ์ด๊ฒฝ๋ฏผ)
  - Backend: 3์ธ(๊นํ์ค, ์์ ๋ฏผ, ์์ฌ๊ฒฝ)
       
## ๐ ํ๋ก์ ํธ ๋ฏธ๋ฆฌ๋ณด๊ธฐ

![](https://images.velog.io/images/anjaekk/post/a48be216-befc-4a4b-903b-db86a34a289a/Jul-26-2021_13-16-47.gif)

## ๐ Database ์ค๊ณ

<details>
<summary>Database modeling</summary>
<div markdown="2">       

![image](https://user-images.githubusercontent.com/74139727/130344978-22559128-4640-45d2-a726-072be9b1fce5.png)

</div>
</details>

## ๐ ๊ตฌํ ๊ธฐ๋ฅ
-Unit test๋ฅผ ํตํ ์ฝ๋ ๊ฒ์ฌ

|User(ํ์๊ฐ์ ๋ฐ ๋ก๊ทธ์ธ)|Product(์ํ ๋ฆฌ์คํธ, ์์ธ๋ณด๊ธฐ)|Contract(์์ฐฐ, ํ๋งค, ๊ณ์ฝ)|
|:-:|:-:|:-:|
|Bcrypt ์ํธํ|pagination|๊ตฌ๋งค์์ ํ๋งค์ ๋์ผ๊ฐ๊ฒฉ ์์ฐฐ ์ฒด๊ฒฐ|
|JWT ์ฌ์ฉ|์นดํ๊ณ ๋ฆฌ๋ณ ์ ๋ ฌ|์์ฐฐ CRUD|
|์นด์นด์ค ๋ก๊ทธ์ธ API|๋ฒ ์คํธ์๊ฐ, ๊ตฌ๋งค, ํ๋งค filtering|
|ํ์๊ฐ์ ์ ํจ์ฑ ๊ฒ์ฌ|์ต๊ทผ ์ฒด๊ฒฐ๊ฑฐ๋ ๊ธฐ๊ฐ๋ณ filtering|
||๊ณ์ฝ๊ธ์ก ๋ณ๋๋ด์ญ ์กฐํ||

## ๐ ๋ด๊ฐ ๊ตฌํํ ๊ธฐ๋ฅ
__*๊ด๋ จ ์ฝ๋ ํ์ธ์ด ๊ฐ๋ฅํฉ๋๋ค__
<details>
<summary>ํ์๊ฐ์ ๋ฐ ๋ก๊ทธ์ธ(Bcrypt ์ํธํ, JWT ์ฌ์ฉ, ์ ๊ทํํ์์ ์ฌ์ฉํ validation)</summary>
<div markdown="1">       

- ํ์๊ฐ์
```
#users.views.py

 REGEX = {
    'email'    : '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
    'password' : '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%#?&])[A-Za-z\d@$!%*#?&]{8,16}$'
}
 
 class SignupView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']
            name         = data['name']

            if not re.match(REGEX['email'], email) or not re.match(REGEX['password'], password):
                return JsonResponse({'message':'INVALID_ERROR'}, status=400)
            
            if User.objects.filter(email=email).exists() or User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'message':'DUPLICATE'},status=409)
            
            encoded_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            User.objects.create(
                email        = email,
                password     = encoded_password.decode('utf-8'),
                phone_number = phone_number,
                name         = name
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)
```

- ๋ก๊ทธ์ธ
```
#users.views.py

class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'INVALID_USER'},status=401)
            
            email    = data['email']
            password = data['password']
            user_id  = User.objects.get(email=email).id

            if bcrypt.checkpw(password.encode('utf-8'), User.objects.get(id=user_id).password.encode('utf-8')):
                access_token = jwt.encode({'user_id':user_id, 'exp':datetime.utcnow()+timedelta(days=1)},SECRET_KEY,algorithm=ALGORITHMS)
                return JsonResponse({'message':'SUCCESS', 'TOKEN':access_token}, status=200)

            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400) 
```

</div>
</details>


<details>
<summary>์นด์นด์ค API๋ฅผ ์ด์ฉํ ์์๋ก๊ทธ์ธ ๊ธฐ๋ฅ ๊ตฌํ</summary>
<div markdown="1">       

```
#users.views.py
  
class KakaoSigninView(View):
    def get(self, request):
        access_token     = request.headers.get('Authorization')
        profile_request  = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"}).json()
        user, is_created = User.objects.get_or_create(kakao_id = profile_request["id"])
        access_token     = jwt.encode({'user_id':user.id, 'exp':datetime.utcnow()+timedelta(days=1)},SECRET_KEY,algorithm=ALGORITHMS)

        if is_created:
            user.email = profile_request['kakao_account']["email"]
            user.save()
            return JsonResponse({'message':'SUCCESS', 'TOKEN':access_token}, status=201)
        return JsonResponse({'message':'SUCCESS', 'TOKEN':access_token}, status=200) 
```


</div>
</details>




<details>
<summary>์ฌ์ฉ์ Authorization</summary>
<div markdown="1">       

```
#utils.py
  
def authorization(func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)

        if not access_token:
            return JsonResponse({'error': 'ACESS_TOKEN_REQUIRED'}, status=401)

        try:
            payload = jwt.decode(access_token, SECRET_KEY, ALGORITHMS)

            if not User.objects.filter(id=payload['user_id']).exists():
                return JsonResponse({'message': 'INVALID_USER'}, satus=400)

            request.user = User.objects.get(id=payload['user_id'])
            return func(self, request, *args, **kwargs)
            

        except jwt.InvalidSignatureError:
            return JsonResponse({'error':'INVALID_TOKEN'}, status=400)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error':'EXPIRED_SIGNATURE'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'error':'INVALID_TOKEN'}, status=401)
            
    return wrapper
```

</div>
</details>

<details>
<summary>์ ํ ์์ธ ์๋ํฌ์ธ๋(์ํ ์ ๋ณด, ์ต๊ทผ ์ฒด๊ฒฐ๊ฑฐ๋ ๊ฐ๊ฒฉ ๊ธฐ๊ฐ๋ณ filtering, ํด๋น ์ํ ์ฒด๊ฒฐ๊ฑฐ๋ ๋ด์ญ ์กฐํ) </summary>
<div markdown="1">       

- ์ต๊ทผ ๊ฑฐ๋๋ด์ญ ๋ฐ ํด๋น ์ํ ๊ฑฐ๋ ์ ๋ณด
```
#products.views.py
class ProductDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'message':'INVALID_ERROR'}, status=404)     
        product = Product.objects.prefetch_related(
            'productcolor_set__color',
            'bidding_set', 
            'productimage_set',
            Prefetch('bidding_set', queryset=Bidding.objects.filter(status_id=1, is_seller=1).order_by('-price', 'created_at'), to_attr="selling_bidding"),
            Prefetch('bidding_set', queryset=Bidding.objects.filter(status_id=1, is_seller=0).order_by('-price', 'created_at'), to_attr="buying_bidding"),
            Prefetch('bidding_set', queryset=Bidding.objects.filter(status_id=1, is_seller=1).order_by('-created_at'), to_attr="selling_bidding_detail"),
            Prefetch('bidding_set', queryset=Bidding.objects.filter(status_id=1, is_seller=0).order_by('-created_at'), to_attr="buying_bidding_detail")
        ).get(id=product_id)

        contract_choice = request.GET.get('contract_choice', '1w')
        contract_period = {
            '3m':datetime.now()-relativedelta(months=3),
            '1m':datetime.now()-relativedelta(months=1),
            '1w':datetime.now()-timedelta(weeks=1)
        }

        contract_all = Contract.objects.select_related('selling_bid__product').filter(selling_bid__product=product_id).order_by('-created_at')
        contracts    = contract_all.filter(created_at__range=(contract_period[contract_choice], datetime.now())).order_by('-created_at')

        if contract_all.count() >= 2:
            latest_price          = contract_all[0].selling_bid.price
            old_price             = contract_all[1].selling_bid.price
            comparing_price       = latest_price - old_price
            comparing_price_ratio = round((comparing_price / old_price) * 100, 1)
        else:
            latest_price = comparing_price = comparing_price_ratio = 0

  main_info = {
            'name'                     : product.name,
            'recent_price'             : contract_all[0].selling_bid.price if contract_all.exists() else 0,
            'oldest_selling_bidding_id': product.selling_bidding[0].id if product.selling_bidding else None,
            'oldest_buying_bidding_id' : product.buying_bidding[0].id if product.buying_bidding else None,
            'current_selling_price'    : product.selling_bidding[0].price if product.selling_bidding else None,
            'current_buying_price'     : product.buying_bidding[0].price if product.buying_bidding else None,
            'image_url'                : [image.image_url for image in product.productimage_set.all()],
            'comparing_price'          : comparing_price,
            'comparing_price_ratio'    : comparing_price_ratio
        }
```
  
- ๊ธฐ๊ฐ๋ณ ๊ฑฐ๋๋ด์ญ ์กฐํ ๋ฐ ์ํ ์ ๋ณด
```
contract_all = [{
            'contract_date' :contract.created_at.strftime('%Y-%m-%d'), 
            'contract_price':contract.selling_bid.price
        } for contract in contract_all]

        contract_detail = [{
            'contract_date' :contract.created_at.strftime('%Y-%m-%d'),
            'contract_price':contract.selling_bid.price
        } for contract in contracts]

        bidding_detail  = {
            'selling_bidding':[{
                'selling_bidding_date' : selling_bidding.created_at.strftime('%Y-%m-%d'),
                'selling_bidding_price' :selling_bidding.price
            } for selling_bidding in product.selling_bidding_detail],
            'buying_bidding':[{
                'buying_bidding_date':buying_bidding.created_at.strftime('%Y-%m-%d'),
                'buying_bidding_price':buying_bidding.price
            } for buying_bidding in product.buying_bidding_detail],
        }

        product_info = {
            'model_number'  :product_id,
            'author'        :product.author.name,
            'color'         :[product_color.color.name for product_color in product.productcolor_set.all()],
            'original_price':product.original_price
        }
        
        return JsonResponse({
            'message'        :'SUCCESS',
            'main_info'      :main_info,
            'contract_detail':contract_detail,
            'contract_all'   :contract_all,
            'bidding_detail' :bidding_detail,
            'product_info'   :product_info},
        status=200)
```


</div>
</details>


## ๐ API Documentation
https://documenter.getpostman.com/view/16450829/TzsZqTM6

## ๐ ํ๋ก์ ํธ ์งํ
<details>
<summary>Trello๋ฅผ ์ด์ฉํ Scrum๊ด๋ฆฌ</summary>
<div markdown="1">       

![image](https://user-images.githubusercontent.com/74139727/130344934-2cd9d61b-26ac-4ced-b90e-3f6335ead0a2.png)


</div>
</details>

- ๋งค์ผ ์ด์  ํ ์ผ, ์ค๋ ํ  ์ผ, ํน์ด์ฌํญ ๊ณต์  stand up meeting ์งํ
- ๋ฏธํ์  Agenda ๊ณต์  
