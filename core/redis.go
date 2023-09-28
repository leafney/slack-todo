/**
 * @Author:      leafney
 * @GitHub:      https://github.com/leafney
 * @Project:     slack-togo
 * @Date:        2023-09-28 08:29
 * @Description:
 */

package core

import (
	rredis "github.com/leafney/rose-redis"
	"github.com/leafney/slack-togo/global"
	"log"
	"os"
)

func InitRedis(stop chan struct{}) {
	redisCfg := global.GConfig.Redis
	client, err := rredis.NewRedis(redisCfg.Addr, &rredis.Option{
		Pwd:  redisCfg.Password,
		Db:   redisCfg.DB,
		Type: rredis.TypeNode,
	})
	if err != nil {
		log.Printf("[Redis] start error %v", err)
		os.Exit(1)
	}

	go func() {
		<-stop // 等待停止信号
		log.Println("[Redis] stop")
		client.Close()
	}()

	log.Println("[Redis] connect success")
	global.GRedis = client
}
