# autoinformer

Автоматический обзвон клиентов клиники с напоминанием даты и возможностью подтвердить, отменить запись


робот в битрикс24 (исходящий вебхук)
```
http://server-ip/call.php?phone={{Контакт: Мобильный телефон}}&deal_date={{Дата и время записи}}&deal_id={{ID}}
```


пример маршрутизации для IVR 

```
[customdests]
include => customdests-custom
exten => dest-2,1,Noop(Entering Custom Destination decline deal)
exten => dest-2,n,Gosub(deal_action,decline,1())
exten => dest-2,n,Noop(Returned from Custom Destination decline deal)
exten => dest-2,n,Goto(play-system-recording,5,1)

exten => dest-3,1,Noop(Entering Custom Destination confirm deal)
exten => dest-3,n,Gosub(deal_action,confirm,1())
exten => dest-3,n,Noop(Returned from Custom Destination confirm deal)
exten => dest-3,n,Goto(play-system-recording,5,1)

;--== end of [customdests] ==--;

```