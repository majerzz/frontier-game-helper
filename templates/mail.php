if(isset($_POST['mess'])){
    //проверки на правильность данных

    $admin_mail = 'shukurovadana@yandex.ru';
    $subj = 'Новое сообщение';
    $mess = htmlspecialchars($_POST['mess']);
    $headers = 'From: site@mail.ru' . PHP_EOL;
    $headers .= 'Content-type: text/plain; charset=utf-8' . PHP_EOL;
}