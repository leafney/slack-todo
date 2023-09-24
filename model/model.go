/**
 * @Author:      leafney
 * @GitHub:      https://github.com/leafney
 * @Project:     slack-togo
 * @Date:        2023-09-23 17:58
 * @Description:
 */

package model

type Slack struct {
	ChannelID string `koanf:"channel_id"`
	BotToken  string `koanf:"bot_token"`
	UserToken string `koanf:"user_token"`
}
