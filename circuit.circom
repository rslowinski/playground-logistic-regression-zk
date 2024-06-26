pragma circom 2.0.0;

template LogisticRegression(n) {
    signal input x[n];
    signal input coef[n];
    signal input intercept;
    signal output y;

    signal int result;
    result <== intercept;
    for (var i = 0; i < n; i++) {
        result <== result + x[i] * coef[i];
    }
    y <== result;
}

component main = LogisticRegression(4);
