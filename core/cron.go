/**
 * @Author:      leafney
 * @GitHub:      https://github.com/leafney
 * @Project:     slack-togo
 * @Date:        2023-10-22 16:36
 * @Description:
 */

package core

import (
	"github.com/go-co-op/gocron"
	"time"
)

func Cron(stop chan struct{}) {
	cron := gocron.NewScheduler(time.UTC)

	//cron.
	//	Cron("*/5 * * * *").
	//	SingletonMode().
	//	WaitForSchedule().
	//	Do(controller.)

	go func() {
		<-stop
		//global.GLog.Infof("[Cron] stop")
		cron.Stop()
	}()

	// 异步启动
	cron.StartAsync()
	//global.GLog.Infof("[Cron] start success")
}
