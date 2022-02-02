def find_n_fib(n):
    ans = [0, 1]
    if n == 0 or n == 1:
        return ans[:n + 1]
    
    for i in range(2, n):
        ans.append(ans[i - 2] + ans[i - 1])
    
    return ans   
