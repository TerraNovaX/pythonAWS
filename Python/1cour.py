

def fizzbuzz(n):
    if n % 3 and n%5 :
        return 'FizzBuzz'
    elif n%3 :
        return 'Fizz'
    elif n%5 : 
        return 'Buzz'
    return n
    

def fibo(n):
    if n==1 : 
        return 1
    elif n==2 : 
        return 1 
    return fibo(n-1) + fibo(n-2) 

def sort_custom (list_number):
    
    res = []
    
    for elm in list_number:
        is_insterted = False
        for idx, item in enumerate(res):
            if elm < item:
                res.insert(idx, elm)
                is_insterted = True
                break
        if not is_insterted:
            res.append(elm)
    return res
    

def main() -> str:
    list1 = [1, 89, 56, 20, 10] 
    resultat = sort_custom(list1)
    print(resultat)
    
    # res1 = filter(lambda x: x<12, list_number)
    # list_number = [
    #     {'premier': 33}, {'deuxieme':56}
    # ]
    
    # result = []
    # for elm in list_number:
    #     if elm < 12 :
    #         result.append(elm)
    
    # print(list(res1))
    
    # for nbr in range(len(list_number)):
    #     print(nbr)
    
    # for nbr, inx in enumerate(list_number):
    #     print(nbr, inx)
    
    # for nbr, inx in enumerate(list_number[2:4]): # permet de couper une liste 
    #     print(nbr, inx)
       
    # list_number_sorted = sorted(list_number)
    # list_number.sort()
    
    # print(list_number)
    
    # for elm in list_number : 
    #     res = fizzbuzz(elm)
    #     print(res)
        
    
    # try:
    #     n: int = int(input()) #input permet de demander à l'utilisateur la donnée
    # except ValueError as error :
    #     print('Enter a digit')
    #     raise ValueError('Enter a digit', error) # obligatoire pour terminé l'essait
    # #print(type(n))
    # result = fizzbuzz(n)
    # print(result)
    
    
if __name__ == '__main__' :
    main()