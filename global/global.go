/**
 * @Author:      leafney
 * @GitHub:      https://github.com/leafney
 * @Project:     slack-togo
 * @Date:        2023-09-23 18:03
 * @Description:
 */

package global

import (
	rredis "github.com/leafney/rose-redis"
	"github.com/leafney/slack-togo/model"
	"gorm.io/gorm"
)

var (
	GConfig *model.Slack
	GRedis  *rredis.Redis
	GDB     *gorm.DB
)
